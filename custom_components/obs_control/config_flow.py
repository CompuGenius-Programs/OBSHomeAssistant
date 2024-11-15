import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "obs_control"


class OBSControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OBS Control."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the input
            try:
                host = user_input["host"]
                port = int(user_input["port"])
                password = user_input["password"]
                # Optionally, validate the connection to OBS here
                return self.async_create_entry(title="OBS Control", data=user_input)
            except Exception as e:
                errors["base"] = "connection_failed"

        data_schema = vol.Schema(
            {vol.Required("host"): str, vol.Required("port", default=4455): int, vol.Required("password"): str, })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
