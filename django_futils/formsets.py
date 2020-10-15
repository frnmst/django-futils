class HasPrimaryInlineFormSet(BaseInlineFormSet):
    r"""Avoid deleting primary objects."""
    def clean(self):
        super().clean()
        for form in self.deleted_forms:
            if form.instance.is_primary:
                raise ValidationError(_('cannot delete primary object'))
