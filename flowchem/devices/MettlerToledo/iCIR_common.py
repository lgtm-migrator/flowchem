from pathlib import Path
from typing import TypedDict


class ProbeInfo(TypedDict):
    spectrometer: str
    spectrometer_SN: str
    probe_SN: str
    detector: str
    apodization: str
    ip_address: str
    probe_type: str
    sampling_interval: str
    resolution: str
    scan_option: str
    gain: str


class IRSpectrometerError(Exception):
    """ General iCIR exceptions (applying both to ReactIR and FlowIR)"""
    pass


class FlowIRError(IRSpectrometerError):
    """ FlowIR specific exceptions """
    pass


# noinspection PyPep8Naming
class iCIR_spectrometer:
    """ Common code between sync and async implementations """
    iC_OPCUA_DEFAULT_SERVER_ADDRESS = "opc.tcp://localhost:62552/iCOpcUaServer"
    _supported_versions = {"7.1.91.0"}
    SOFTWARE_VERSION = "ns=2;s=Local.iCIR.SoftwareVersion"
    CONNECTION_STATUS = "ns=2;s=Local.iCIR.ConnectionStatus"
    PROBE_DESCRIPTION = "ns=2;s=Local.iCIR.Probe1.ProbeDescription"
    PROBE_STATUS = "ns=2;s=Local.iCIR.Probe1.ProbeStatus"
    LAST_SAMPLE_TIME = "ns=2;s=Local.iCIR.Probe1.LastSampleTime"
    SAMPLE_COUNT = "ns=2;s=Local.iCIR.Probe1.SampleCount"
    SPECTRA_TREATED = "ns=2;s=Local.iCIR.Probe1.SpectraTreated"
    SPECTRA_RAW = "ns=2;s=Local.iCIR.Probe1.SpectraRaw"
    SPECTRA_BACKGROUND = "ns=2;s=Local.iCIR.Probe1.SpectraBackground"
    START_EXPERIMENT = "ns=2;s=Local.iCIR.Probe1.Methods.Start Experiment"
    STOP_EXPERIMENT = "ns=2;s=Local.iCIR.Probe1.Methods.Stop"
    METHODS = "ns=2;s=Local.iCIR.Probe1.Methods"

    def is_local(self):
        """ Returns true if the server is on the same machine running the python code. """
        return any(x in self.opcua.aio_obj.server_url.netloc for x in ("localhost", "127.0.0.1"))

    @staticmethod
    def _normalize_template_name(template_name) -> str:
        """ Adds .iCIRTemplate extension from string if not already present """
        return (
            template_name
            if template_name.endswith(".iCIRTemplate")
            else template_name + ".iCIRTemplate"
        )

    @staticmethod
    def is_template_name_valid(template_name: str) -> bool:
        """
        From Mettler Toledo docs:
        You can use the Start method to create and run a new experiment in one of the iC analytical applications
        (i.e. iC IR, iC FBRM, iC Vision, iC Raman). Note that you must provide the name of an existing experiment
        template file that can be used as a basis for the new experiment.
        The template file must be located in a specific folder on the iC OPC UA Server computer.
        This is usually C:\\ProgramData\\METTLER TOLEDO\\iC OPC UA Server\\1.2\\Templates.
        """

        template_directory = Path(
            r"C:\ProgramData\METTLER TOLEDO\iC OPC UA Server\1.2\Templates"
        )
        if not template_directory.exists() or not template_directory.is_dir():
            raise IRSpectrometerError("iCIR template folder not found!")

        # Ensures the name has been provided with no extension (common mistake)
        template_name = iCIR_spectrometer._normalize_template_name(template_name)
        for existing_template in template_directory.glob("*.iCIRTemplate"):
            if existing_template.name == template_name:
                return True
        return False

    @staticmethod
    def parse_probe_info(probe_info: str) -> ProbeInfo:
        # 'FlowIR; SN: 2989; Detector: DTGS; Apodization: HappGenzel; IP Address: 192.168.1.2;
        # Probe: DiComp (Diamond); SN: 14570173; Interface: FlowIR™ Sensor; Sampling: 4000 to 650 cm-1;
        # Resolution: 8; Scan option: AutoSelect; Gain: 232;'
        fields = probe_info.split(";")
        probe_info = {
            "spectrometer": fields[0],
            "spectrometer_SN": fields[1].split(": ")[1],
            "probe_SN": fields[6].split(": ")[1],
        }

        # Use aliases, i.e. translate API names (left) to dict key (right)
        translate_attributes = {
            "Detector": "detector",
            "Apodization": "apodization",
            "IP Address": "ip_address",
            "Probe": "probe_type",
            "Sampling": "sampling_interval",
            "Resolution": "resolution",
            "Scan option": "scan_option",
            "Gain": "gain",
        }
        for element in fields:
            if ":" in element:
                piece = element.split(":")
                if piece[0].strip() in translate_attributes:
                    probe_info[translate_attributes[piece[0].strip()]] = piece[
                        1
                    ].strip()

        return probe_info