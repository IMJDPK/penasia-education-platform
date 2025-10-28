#!/bin/bash

# Script to remove all CEF references from PenAsia website
echo "Removing CEF references from website..."

# Remove CEF from application forms
sed -i "s/('cef', 'CEF Reimbursement'),//g" "/home/imjd/Hong Kong University/Flask Website/forms.py"
sed -i "s/cef_application = BooleanField('Apply for Continuing Education Fund (CEF) Subsidy')//g" "/home/imjd/Hong Kong University/Flask Website/forms.py"
sed -i "s/hkid_number = StringField('Hong Kong ID Number (Required for CEF)', validators=\[Optional(), Length(max=20)\])//g" "/home/imjd/Hong Kong University/Flask Website/forms.py"
sed -i "s/cef_eligible = BooleanField('CEF Eligible')//g" "/home/imjd/Hong Kong University/Flask Website/forms.py"
sed -i "s/cef_fee_hkd = DecimalField('CEF Fee (HKD)', validators=\[Optional(), NumberRange(min=0)\])//g" "/home/imjd/Hong Kong University/Flask Website/forms.py"
sed -i "s/('financial_aid', 'Financial Aid & CEF Information'),/('financial_aid', 'Financial Aid Information'),/g" "/home/imjd/Hong Kong University/Flask Website/forms.py"

# Remove CEF validation
sed -i "/if self.cef_application.data and not hkid_number.data:/,+1d" "/home/imjd/Hong Kong University/Flask Website/forms.py"

# Remove CEF from payment service
sed -i "s/'cef',//g" "/home/imjd/Hong Kong University/Flask Website/payment_service.py"
sed -i "/elif payment_method == 'cef':/,+2d" "/home/imjd/Hong Kong University/Flask Website/payment_service.py"
sed -i "/'cef': {/,+2d" "/home/imjd/Hong Kong University/Flask Website/payment_service.py"

echo "CEF references removal script completed!"
