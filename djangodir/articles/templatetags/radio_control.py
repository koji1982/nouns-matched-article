from django import template
import structlog

register = template.Library()

@register.filter(name='call_function')
def call_function(string):
    logger = structlog.get_logger(__name__)
    logger.info('   templatetag !!!' + string)

@register.filter(name='is_checked')
def is_checked(id):
    logger = structlog.get_logger(__name__)
    logger.info(id)
    return True