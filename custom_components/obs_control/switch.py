from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from obsws_python import ReqClient

DOMAIN = "obs_control"


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up OBS Control switches."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    switch = OBSControlSwitch(data["host"], data["port"], data["password"])
    async_add_entities([switch])

    # Register a service to call process_filename
    async def handle_process_filename(call):
        filename = call.data.get("filename")
        await switch.process_filename(filename)

    hass.services.async_register(DOMAIN, "process_filename", handle_process_filename)


class OBSControlSwitch(SwitchEntity):
    """Representation of the OBS Control switch."""

    def __init__(self, host, port, password):
        """Initialize the switch."""
        self._host = host
        self._port = port
        self._password = password
        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return "OBS Control"

    @property
    def is_on(self):
        """Return the switch status."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn on the stream."""
        await self._set_streaming(True)

    async def async_turn_off(self, **kwargs):
        """Turn off the stream."""
        await self._set_streaming(False)

    async def async_update(self):
        """Fetch the latest status from OBS."""
        self._is_on = await self._is_streaming()

    async def _is_streaming(self):
        try:
            with ReqClient(host=self._host, port=self._port, password=self._password) as client:
                return client.get_stream_status().output_active
        except Exception:
            return False

    async def _set_streaming(self, start):
        try:
            with ReqClient(host=self._host, port=self._port, password=self._password) as client:
                client.start_stream() if start else client.stop_stream()
        except Exception as e:
            self._is_on = await self._is_streaming()

    async def process_filename(self, filename):
        with ReqClient(host=self._host, port=self._port, password=self._password) as client:
            client.send("SetInputSettings", {"inputName": "Filename", "inputSettings": {"text": filename}})
