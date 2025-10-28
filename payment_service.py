"""
Payment processing system for PenAsia
Handles payment integration and tracking
"""
from datetime import datetime
import uuid
import hashlib

class PaymentProcessor:
    def __init__(self):
        self.supported_methods = ['credit_card', 'bank_transfer', 'cef', 'installments']
        self.currency = 'HKD'
    
    def generate_payment_reference(self, user_id, course_id, amount):
        """Generate unique payment reference"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data = f"{user_id}-{course_id}-{amount}-{timestamp}"
        hash_object = hashlib.md5(data.encode())
        return f"PA{timestamp}{hash_object.hexdigest()[:6].upper()}"
    
    def calculate_installment_schedule(self, total_amount, num_installments=3):
        """Calculate installment payment schedule"""
        if num_installments <= 1:
            return [{'amount': total_amount, 'due_date': datetime.now()}]
        
        installment_amount = total_amount / num_installments
        schedule = []
        
        for i in range(num_installments):
            # For demo purposes, installments are due monthly
            due_date = datetime.now().replace(day=1)
            if i > 0:
                # Add months (simplified calculation)
                month = due_date.month + i
                year = due_date.year
                if month > 12:
                    month -= 12
                    year += 1
                due_date = due_date.replace(month=month, year=year)
            
            schedule.append({
                'installment_number': i + 1,
                'amount': round(installment_amount, 2),
                'due_date': due_date,
                'status': 'pending'
            })
        
        return schedule
    
    def process_payment(self, user, course, amount, payment_method, application_id):
        """Process payment (simulation for demo purposes)"""
        reference = self.generate_payment_reference(user.id, course.id, amount)
        
        # Simulate payment processing
        payment_data = {
            'reference': reference,
            'amount': amount,
            'currency': self.currency,
            'method': payment_method,
            'status': 'completed',  # In real system, this would be 'pending' initially
            'processed_at': datetime.now(),
            'user_id': user.id,
            'course_id': course.id,
            'application_id': application_id
        }
        
        # For installments, create schedule
        if payment_method == 'installments':
            payment_data['installment_schedule'] = self.calculate_installment_schedule(amount)
            payment_data['status'] = 'partial'  # First installment
        
        # Simulate different payment methods
        if payment_method == 'credit_card':
            payment_data['gateway'] = 'stripe'
            payment_data['transaction_id'] = f"txn_{uuid.uuid4().hex[:12]}"
        elif payment_method == 'bank_transfer':
            payment_data['bank_account'] = "HSBC HK - Account: 123-456789-001"
            payment_data['status'] = 'pending'  # Bank transfers need verification
        elif payment_method == 'cef':
            payment_data['cef_reference'] = f"CEF{datetime.now().strftime('%Y%m%d')}{user.id:04d}"
            payment_data['cef_amount'] = min(amount * 0.8, 25000)  # 80% up to HK$25,000
        
        return payment_data
    
    def get_payment_instructions(self, payment_method, amount, reference):
        """Get payment instructions for different methods"""
        instructions = {
            'credit_card': {
                'title': 'Credit Card Payment',
                'description': 'Your card will be charged immediately.',
                'steps': [
                    'Click the "Pay Now" button below',
                    'Enter your credit card details securely',
                    'Confirm the payment',
                    'You will receive a confirmation email'
                ]
            },
            'bank_transfer': {
                'title': 'Bank Transfer',
                'description': f'Please transfer HK${amount:,.0f} to our bank account.',
                'steps': [
                    'Bank: HSBC Hong Kong',
                    'Account Name: PenAsia Continuing Education Centre Limited',
                    'Account Number: 123-456789-001',
                    f'Reference: {reference}',
                    'Send proof of transfer to finance@penasia.edu.hk'
                ]
            },
            'installments': {
                'title': 'Installment Payment',
                'description': f'Pay HK${amount:,.0f} in 3 monthly installments.',
                'steps': [
                    f'First installment: HK${amount/3:,.0f} (due immediately)',
                    f'Second installment: HK${amount/3:,.0f} (due next month)',
                    f'Third installment: HK${amount/3:,.0f} (due in 2 months)',
                    'Payment reminders will be sent via email'
                ]
            },
            'cef': {
                'title': 'CEF Reimbursement',
                'description': 'Pay full amount first, then claim CEF reimbursement.',
                'steps': [
                    f'Pay full amount: HK${amount:,.0f}',
                    'Complete the course with 80% attendance',
                    'Apply for CEF reimbursement online',
                    f'Receive up to HK${min(amount * 0.8, 25000):,.0f} reimbursement'
                ]
            }
        }
        
        return instructions.get(payment_method, {
            'title': 'Payment Required',
            'description': 'Please contact us for payment arrangements.',
            'steps': ['Call (852) 2529 6138 for assistance']
        })

# Initialize payment processor
payment_processor = PaymentProcessor()
