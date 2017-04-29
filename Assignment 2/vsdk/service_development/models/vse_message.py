from django.db import models

from .vs_element import VoiceServiceElement


class MessagePresentation(VoiceServiceElement):
    """
    An element that presents a Voice Label to the user.
    """
    _urls_name = 'service-development:message-presentation'
    final_element = models.BooleanField('This element will terminate the call', default=False)
    _redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        help_text="The element to redirect to after the message has been played.")

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._redirect.id)
        else:
            return None

    def __str__(self):
        return "Message: " + self.name

    def is_valid(self):
        return len(self.validator()) == 0

    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(MessagePresentation, self).validator())
        if not self.final_element and not self._redirect:
            errors.append('Message %s does not have a redirect element and is not a final element' % self.name)
        elif not self.final_element:
            if self._redirect.id == self.id:
                errors.append('!!!! There is a loop in %s' % str(self))
            else:
                errors.extend(self._redirect.validator())

        return errors
