from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message
from models import get_content, CarouselImage, ContactMessage
from app import db, mail
import logging

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    carousel_images = CarouselImage.query.filter_by(is_active=True).order_by(CarouselImage.order_index).all()
    
    content = {
        'hero_title': get_content('home', 'hero_title'),
        'hero_subtitle': get_content('home', 'hero_subtitle'),
        'hero_description': get_content('home', 'hero_description'),
        'stats_countries': get_content('home', 'stats_countries'),
        'stats_calls': get_content('home', 'stats_calls'),
        'stats_uptime': get_content('home', 'stats_uptime'),
        'stats_customers': get_content('home', 'stats_customers')
    }
    
    features = {
        'section_title': get_content('features', 'section_title'),
        'section_subtitle': get_content('features', 'section_subtitle'),
        'feature1_title': get_content('features', 'feature1_title'),
        'feature1_desc': get_content('features', 'feature1_desc'),
        'feature2_title': get_content('features', 'feature2_title'),
        'feature2_desc': get_content('features', 'feature2_desc'),
        'feature3_title': get_content('features', 'feature3_title'),
        'feature3_desc': get_content('features', 'feature3_desc'),
        'feature4_title': get_content('features', 'feature4_title'),
        'feature4_desc': get_content('features', 'feature4_desc'),
        'feature5_title': get_content('features', 'feature5_title'),
        'feature5_desc': get_content('features', 'feature5_desc'),
        'feature6_title': get_content('features', 'feature6_title'),
        'feature6_desc': get_content('features', 'feature6_desc')
    }
    
    cta = {
        'title': get_content('cta', 'title'),
        'subtitle': get_content('cta', 'subtitle')
    }
    
    return render_template('index.html', content=content, features=features, cta=cta, carousel_images=carousel_images)

@main_bp.route('/about')
def about():
    content = {
        'title': get_content('about', 'title'),
        'description': get_content('about', 'description'),
        'mission': get_content('about', 'mission'),
        'vision': get_content('about', 'vision'),
        'founded_year': get_content('about', 'founded_year'),
        'team_size': get_content('about', 'team_size'),
        'experience': get_content('about', 'experience')
    }
    
    return render_template('about.html', content=content)

@main_bp.route('/services')
def services():
    content = {
        'title': get_content('services', 'title'),
        'description': get_content('services', 'description'),
        'service1_title': get_content('services', 'service1_title'),
        'service1_desc': get_content('services', 'service1_desc'),
        'service2_title': get_content('services', 'service2_title'),
        'service2_desc': get_content('services', 'service2_desc'),
        'service3_title': get_content('services', 'service3_title'),
        'service3_desc': get_content('services', 'service3_desc'),
        'service4_title': get_content('services', 'service4_title'),
        'service4_desc': get_content('services', 'service4_desc'),
        'service5_title': get_content('services', 'service5_title'),
        'service5_desc': get_content('services', 'service5_desc'),
        'service6_title': get_content('services', 'service6_title'),
        'service6_desc': get_content('services', 'service6_desc')
    }
    
    return render_template('services.html', content=content)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone', '')
            subject = request.form.get('subject')
            message_text = request.form.get('message')
            
            # Validate required fields
            if not all([name, email, subject, message_text]):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('main.contact'))
            
            # Save message to database
            contact_message = ContactMessage()
            contact_message.name = name
            contact_message.email = email
            contact_message.phone = phone
            contact_message.subject = subject
            contact_message.message = message_text
            db.session.add(contact_message)
            db.session.commit()
            
            # Send email notification (if configured)
            try:
                msg = Message(
                    subject=f'VoipFit Contact: {subject}',
                    recipients=[get_content('contact', 'email', 'info@voipfit.com')],
                    body=f'''
New contact message from VoipFit website:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message_text}
                    '''
                )
                mail.send(msg)
                logging.info(f'Contact email sent for message from {email}')
            except Exception as e:
                logging.error(f'Failed to send contact email: {str(e)}')
            
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            logging.error(f'Error processing contact form: {str(e)}')
            flash('An error occurred while sending your message. Please try again.', 'error')
            return redirect(url_for('main.contact'))
    
    content = {
        'title': get_content('contact', 'title'),
        'description': get_content('contact', 'description'),
        'address': get_content('contact', 'address'),
        'phone': get_content('contact', 'phone'),
        'email': get_content('contact', 'email'),
        'hours': get_content('contact', 'hours')
    }
    
    return render_template('contact.html', content=content)
