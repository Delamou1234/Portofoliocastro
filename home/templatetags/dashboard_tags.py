from django import template

register = template.Library()

@register.filter
def count_featured(projects):
    """Compte le nombre de projets en vedette."""
    if not projects:
        return 0
    return sum(1 for p in projects if getattr(p, 'featured', False))
