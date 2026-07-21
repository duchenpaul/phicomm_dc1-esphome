import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import i2c
from esphome.const import (
    CONF_ID,
    CONF_INPUT,
    CONF_INVERTED,
    CONF_MODE,
    CONF_NUMBER,
    CONF_OUTPUT,
)

DEPENDENCIES = ["i2c"]
MULTI_CONF = True

cat9554_ns = cg.esphome_ns.namespace("cat9554")
CAT9554GPIOMode = cat9554_ns.enum("CAT9554GPIOMode")
CAT9554_GPIO_MODES = {
    "INPUT": CAT9554GPIOMode.CAT9554_INPUT,
    "OUTPUT": CAT9554GPIOMode.CAT9554_OUTPUT,
}

CAT9554Component = cat9554_ns.class_("CAT9554Component", cg.Component, i2c.I2CDevice)
CAT9554GPIOPin = cat9554_ns.class_("CAT9554GPIOPin", cg.GPIOPin)

CONF_CAT9554 = "cat9554"
CONF_IRQ_PIN = "irq_pin"
CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(CAT9554Component),
            cv.Optional(CONF_IRQ_PIN): pins.internal_gpio_input_pin_schema,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(i2c.i2c_device_schema(0x20))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    if CONF_IRQ_PIN in config:
        irq_pin = await cg.gpio_pin_expression(config[CONF_IRQ_PIN])
        cg.add(var.set_irq_pin(irq_pin))
    await i2c.register_i2c_device(var, config)


def validate_mode(value):
    if not (value[CONF_INPUT] or value[CONF_OUTPUT]):
        raise cv.Invalid("Mode must be either input or output")
    if value[CONF_INPUT] and value[CONF_OUTPUT]:
        raise cv.Invalid("Mode must be either input or output")
    return value


CAT9554_PIN_SCHEMA = pins.gpio_base_schema(
    CAT9554GPIOPin,
    cv.int_range(min=0, max=7),
    modes=[CONF_INPUT, CONF_OUTPUT],
    mode_validator=validate_mode,
    invertible=True,
).extend(
    {
        cv.Required(CONF_CAT9554): cv.use_id(CAT9554Component),
    }
)


@pins.PIN_SCHEMA_REGISTRY.register(CONF_CAT9554, CAT9554_PIN_SCHEMA)
async def cat9554_pin_to_code(config):
    parent = await cg.get_variable(config[CONF_CAT9554])
    mode = (
        CAT9554GPIOMode.CAT9554_INPUT
        if config[CONF_MODE][CONF_INPUT]
        else CAT9554GPIOMode.CAT9554_OUTPUT
    )
    return cg.new_Pvariable(
        config[CONF_ID],
        parent,
        config[CONF_NUMBER],
        mode,
        config[CONF_INVERTED],
    )
