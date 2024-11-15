from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "obs_control"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up OBS Control from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "switch"))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload OBS Control config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "switch")
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
