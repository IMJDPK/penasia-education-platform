# CONTACT FORM FIX - Implementation Guide

## Problem
The contact form in `templates/contact.html` has no backend processing. Form submissions are not saved or processed.

## Solution

### Step 1: Create ContactInquiry Model

Add to `models.py`:

```python
class ContactInquiry(db.Model):
    """Contact form inquiries"""
    __tablename__ = 'contact_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    program_interest = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    subscribe_newsletter = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='new')  # new, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_notes = db.Column(db.Text)
    
    # Relationship
    resolved_by = db.relationship('User', backref='resolved_inquiries', foreign_keys=[resolved_by_id])
    
    def __repr__(self):
        return f'<ContactInquiry {self.id}: {self.first_name} {self.last_name} - {self.subject}>'
```

### Step 2: Create ContactForm

Add to `forms.py`:

```python
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    """Contact form"""
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=100, message='First name must be between 2 and 100 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=100, message='Last name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number', validators=[
        Length(max=20, message='Phone number must be less than 20 characters')
    ])
    subject = SelectField('Subject', validators=[
        DataRequired(message='Please select a subject')
    ], choices=[
        ('', 'Choose a subject...'),
        ('general', 'General Inquiry'),
        ('admissions', 'Admissions Information'),
        ('programs', 'Program Details'),
        ('facilities', 'Facilities Tour'),
        ('fees', 'Fees and Payment'),
        ('cef', 'CEF Information'),
        ('other', 'Other')
    ])
    program_interest = SelectField('Program of Interest', choices=[
        ('', 'Select a program...'),
        ('169', 'Hotel Culinary Management Diploma'),
        ('btec', 'BTEC Business Management'),
        ('171', 'Western Bakery & Pastry Certificate'),
        ('179', 'Western Cuisine Certificate')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=2000, message='Message must be between 10 and 2000 characters')
    ])
    subscribe_newsletter = BooleanField('I would like to receive updates about programs and events')
    submit = SubmitField('Send Message')
```

### Step 3: Update Contact Route in app.py

Replace the current contact route (line ~1344):

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create inquiry record
        inquiry = ContactInquiry(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            program_interest=form.program_interest.data,
            message=form.message.data,
            subscribe_newsletter=form.subscribe_newsletter.data
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        # Create admin notifications
        admin_users = User.query.filter_by(role='admin').all()
        for admin in admin_users:
            notification = Notification(
                user_id=admin.id,
                type='contact',
                title=f'New Contact Inquiry: {form.subject.data}',
                message=f'{form.first_name.data} {form.last_name.data} ({form.email.data}) has sent a message via the contact form. Subject: {form.subject.data}',
                link_url=f'/admin/contact-inquiries',
                priority='medium'
            )
            db.session.add(notification)
        
        db.session.commit()
        
        # Optional: Send email notification
        try:
            send_contact_confirmation_email(form.email.data, form.first_name.data)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        flash('Thank you for contacting us! We will respond within 24-48 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)
```

### Step 4: Update contact.html Template

Replace the form section (lines 28-89) with:

```html
<form method="POST" action="{{ url_for('contact') }}">
    {{ form.csrf_token }}
    
    {% if form.errors %}
    <div class="alert alert-danger">
        <strong>Please correct the following errors:</strong>
        <ul>
        {% for field, errors in form.errors.items() %}
            {% for error in errors %}
            <li>{{ error }}</li>
            {% endfor %}
        {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <div class="row">
        <div class="col-md-6 mb-3">
            {{ form.first_name.label(class="form-label") }}
            {{ form.first_name(class="form-control" ~ (" is-invalid" if form.first_name.errors else "")) }}
            {% if form.first_name.errors %}
            <div class="invalid-feedback">{{ form.first_name.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="col-md-6 mb-3">
            {{ form.last_name.label(class="form-label") }}
            {{ form.last_name(class="form-control" ~ (" is-invalid" if form.last_name.errors else "")) }}
            {% if form.last_name.errors %}
            <div class="invalid-feedback">{{ form.last_name.errors[0] }}</div>
            {% endif %}
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-3">
            {{ form.email.label(class="form-label") }}
            {{ form.email(class="form-control" ~ (" is-invalid" if form.email.errors else ""), type="email") }}
            {% if form.email.errors %}
            <div class="invalid-feedback">{{ form.email.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="col-md-6 mb-3">
            {{ form.phone.label(class="form-label") }}
            {{ form.phone(class="form-control" ~ (" is-invalid" if form.phone.errors else ""), type="tel") }}
            {% if form.phone.errors %}
            <div class="invalid-feedback">{{ form.phone.errors[0] }}</div>
            {% endif %}
        </div>
    </div>
    
    <div class="mb-3">
        {{ form.subject.label(class="form-label") }}
        {{ form.subject(class="form-select" ~ (" is-invalid" if form.subject.errors else "")) }}
        {% if form.subject.errors %}
        <div class="invalid-feedback">{{ form.subject.errors[0] }}</div>
        {% endif %}
    </div>
    
    <div class="mb-3">
        {{ form.program_interest.label(class="form-label") }}
        {{ form.program_interest(class="form-select" ~ (" is-invalid" if form.program_interest.errors else "")) }}
    </div>
    
    <div class="mb-3">
        {{ form.message.label(class="form-label") }}
        {{ form.message(class="form-control" ~ (" is-invalid" if form.message.errors else ""), rows=5, placeholder="Please tell us how we can help you...") }}
        {% if form.message.errors %}
        <div class="invalid-feedback">{{ form.message.errors[0] }}</div>
        {% endif %}
    </div>
    
    <div class="mb-3 form-check">
        {{ form.subscribe_newsletter(class="form-check-input") }}
        {{ form.subscribe_newsletter.label(class="form-check-label") }}
    </div>
    
    {{ form.submit(class="btn btn-primary btn-lg") }}
</form>
```

### Step 5: Create Admin View for Contact Inquiries

Add to `app.py`:

```python
@app.route('/admin/contact-inquiries')
@login_required
def admin_contact_inquiries():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get inquiries with filters
    status_filter = request.args.get('status', 'all')
    
    query = ContactInquiry.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    inquiries = query.order_by(ContactInquiry.created_at.desc()).all()
    
    return render_template('admin/contact_inquiries.html', inquiries=inquiries, status_filter=status_filter)

@app.route('/admin/contact-inquiry/<int:inquiry_id>/update', methods=['POST'])
@login_required
def update_contact_inquiry(inquiry_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    inquiry = ContactInquiry.query.get_or_404(inquiry_id)
    
    action = request.form.get('action')
    
    if action == 'resolve':
        inquiry.status = 'resolved'
        inquiry.resolved_at = datetime.utcnow()
        inquiry.resolved_by_id = current_user.id
        inquiry.admin_notes = request.form.get('admin_notes', '')
        flash('Contact inquiry marked as resolved', 'success')
    
    elif action == 'in_progress':
        inquiry.status = 'in_progress'
        flash('Contact inquiry marked as in progress', 'success')
    
    elif action == 'reopen':
        inquiry.status = 'new'
        inquiry.resolved_at = None
        inquiry.resolved_by_id = None
        flash('Contact inquiry reopened', 'success')
    
    db.session.commit()
    return redirect(url_for('admin_contact_inquiries'))
```

### Step 6: Create Database Migration

```bash
cd "/home/imjd/Hong Kong University/Flask Website"
source flask_env/bin/activate
flask db migrate -m "Add contact inquiries table"
flask db upgrade
```

### Step 7: Test the Implementation

1. Restart Flask server
2. Navigate to `/contact`
3. Fill out form with valid data
4. Submit and verify:
   - Success message appears
   - Redirected back to contact page
   - Login as admin → Check notifications
   - Go to `/admin/contact-inquiries` → See the inquiry

## Email Service (Optional)

Add to `email_service.py`:

```python
def send_contact_confirmation_email(recipient_email, first_name):
    """Send confirmation email after contact form submission"""
    subject = "Thank You for Contacting PenAsia"
    
    html_body = f"""
    <h2>Thank You for Your Inquiry</h2>
    <p>Dear {first_name},</p>
    <p>We have received your message and appreciate you reaching out to PenAsia Continuing Education Centre.</p>
    <p>Our admissions team will review your inquiry and respond within 24-48 business hours.</p>
    <p>In the meantime, feel free to explore our programs at <a href="https://penasia.edu.hk">penasia.edu.hk</a></p>
    <br>
    <p>Best regards,<br>
    PenAsia Admissions Team</p>
    """
    
    send_email(
        subject=subject,
        recipients=[recipient_email],
        html_body=html_body
    )
```

## Estimated Time: 30-45 minutes

This implementation will:
- ✓ Save contact form submissions to database
- ✓ Create admin notifications
- ✓ Display validation errors to users
- ✓ Send confirmation email (optional)
- ✓ Provide admin interface to manage inquiries
