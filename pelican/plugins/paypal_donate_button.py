# -*- coding: utf-8 -*-
"""
    Copyright (c) Olivier Crave <cravesoft@gmail.com>

    A plugin to add a PayPal's Donation button to collect donations on your website.
    
    To enable it set in your pelican config file the PAYPAL_PKCS7 parameter to your encrypted key.

    in your template just use the {{...}} syntax in jinja2 against the
    paypal_donate_button variable.

    i.e.

        <div class="social">
            {{ paypal_donate_button }}
        </div>
"""

from pelican import signals


class PayPalDonateButton():
    import textwrap
    FORM_HTML = textwrap.dedent("""\
            <form action="https://www.paypal.com/cgi-bin/webscr" method="post">
                <input type="hidden" name="cmd" value="_s-xclick">
                <input type="hidden" name="encrypted" value="{0}">
                <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
                <img alt="" border="0" src="https://www.paypalobjects.com/fr_FR/i/scr/pixel.gif" width="1" height="1">
            </form>""")

    """
        A class created to generate PayPal's html snippet
    """
    def __init__(self, generator):
        self.pkcs7 = generator.settings['PAYPAL_PKCS7']

    def get_paypal(self):
        """
            returns PayPal's html snippet
        """

        return self.FORM_HTML.format(self.pkcs7)


def get_paypal_donate_button(gen, metadata):
    """
        registered handler for the paypal donate button plugin
        it puts in generator.context the html needed to be displayed on a
        template
    """

    if 'PAYPAL_PKCS7' in gen.settings.keys():
        gen.context['paypal_donate_button'] = gen.plugin_instance.get_paypal()


def paypal_donate_button_initialization(generator):
    """
        Initialization of the plugin
    """

    generator.plugin_instance = PayPalDonateButton(generator)


def register():
    """
        Plugin registration
    """
    signals.article_generator_init.connect(paypal_donate_button_initialization)
    signals.article_generate_context.connect(get_paypal_donate_button)
