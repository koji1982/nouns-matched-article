import structlog
from scraping.words import callFunctionTest
from django import template
register = template.Library()

@register.filter(name='apply_choice')
def aplly_choice(request):
    logger = structlog.get_logger(__name__)
    logger.info("from external_functions")
    if request.method == "POST":
        logger.info(request.method)
    callFunctionTest()

