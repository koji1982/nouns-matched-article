import structlog
from scraping.analysis import callFunctionTest
from django import template
register = template.Library()

@register.filter(name='reflect_choice')
def reflect_choice(request):
    logger = structlog.get_logger(__name__)
    logger.info("from external_functions")
    if request.method == "POST":
        logger.info(request.method)
    callFunctionTest()

