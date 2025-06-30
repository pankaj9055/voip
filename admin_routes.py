from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import Admin, Content, CarouselImage, ContactMessage, get_content, set_content
from app import db
import os
import logging

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    total_carousel_images = CarouselImage.query.filter_by(is_active=True).count()
    total_content_items = Content.query.count()
    
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    stats = {
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'total_carousel_images': total_carousel_images,
        'total_content_items': total_content_items
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_messages=recent_messages)

@admin_bp.route('/content')
@admin_bp.route('/content/<section>')
@login_required
def content(section='home'):
    sections = ['home', 'about', 'services', 'contact']
    content_items = Content.query.filter_by(section=section).all()
    return render_template('admin/content.html', content_items=content_items, section=section, sections=sections)

@admin_bp.route('/content/update', methods=['POST'])
@login_required
def update_content():
    try:
        section = request.form.get('section')
        key = request.form.get('key')
        value = request.form.get('value')
        content_type = request.form.get('content_type', 'text')
        
        if not all([section, key, value]):
            flash('All fields are required.', 'error')
            return redirect(url_for('admin.content', section=section))
        
        set_content(section, key, value, content_type)
        flash('Content updated successfully!', 'success')
        
    except Exception as e:
        logging.error(f'Error updating content: {str(e)}')
        flash('An error occurred while updating content.', 'error')
    
    return redirect(url_for('admin.content', section=section))

@admin_bp.route('/content/add', methods=['POST'])
@login_required
def add_content():
    try:
        section = request.form.get('section')
        key = request.form.get('key')
        value = request.form.get('value')
        content_type = request.form.get('content_type', 'text')
        
        if not all([section, key, value]):
            flash('All fields are required.', 'error')
            return redirect(url_for('admin.content', section=section))
        
        # Check if content already exists
        existing = Content.query.filter_by(section=section, key=key).first()
        if existing:
            flash('Content with this key already exists in this section.', 'error')
            return redirect(url_for('admin.content', section=section))
        
        content = Content(section=section, key=key, value=value, content_type=content_type)
        db.session.add(content)
        db.session.commit()
        
        flash('Content added successfully!', 'success')
        
    except Exception as e:
        logging.error(f'Error adding content: {str(e)}')
        flash('An error occurred while adding content.', 'error')
    
    return redirect(url_for('admin.content', section=section))

@admin_bp.route('/content/delete/<int:content_id>')
@login_required
def delete_content(content_id):
    try:
        content = Content.query.get_or_404(content_id)
        section = content.section
        db.session.delete(content)
        db.session.commit()
        flash('Content deleted successfully!', 'success')
    except Exception as e:
        logging.error(f'Error deleting content: {str(e)}')
        flash('An error occurred while deleting content.', 'error')
    
    return redirect(url_for('admin.content', section=section))

@admin_bp.route('/images')
@login_required
def images():
    carousel_images = CarouselImage.query.order_by(CarouselImage.order_index).all()
    return render_template('admin/images.html', carousel_images=carousel_images)

@admin_bp.route('/images/add', methods=['POST'])
@login_required
def add_image():
    try:
        title = request.form.get('title')
        image_url = request.form.get('image_url')
        order_index = int(request.form.get('order_index', 0))
        
        if not all([title, image_url]):
            flash('Title and image URL are required.', 'error')
            return redirect(url_for('admin.images'))
        
        image = CarouselImage(title=title, image_url=image_url, order_index=order_index)
        db.session.add(image)
        db.session.commit()
        
        flash('Image added successfully!', 'success')
        
    except Exception as e:
        logging.error(f'Error adding image: {str(e)}')
        flash('An error occurred while adding image.', 'error')
    
    return redirect(url_for('admin.images'))

@admin_bp.route('/images/update/<int:image_id>', methods=['POST'])
@login_required
def update_image(image_id):
    try:
        image = CarouselImage.query.get_or_404(image_id)
        
        image.title = request.form.get('title', image.title)
        image.image_url = request.form.get('image_url', image.image_url)
        image.order_index = int(request.form.get('order_index', image.order_index))
        image.is_active = 'is_active' in request.form
        
        db.session.commit()
        flash('Image updated successfully!', 'success')
        
    except Exception as e:
        logging.error(f'Error updating image: {str(e)}')
        flash('An error occurred while updating image.', 'error')
    
    return redirect(url_for('admin.images'))

@admin_bp.route('/images/delete/<int:image_id>')
@login_required
def delete_image(image_id):
    try:
        image = CarouselImage.query.get_or_404(image_id)
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully!', 'success')
    except Exception as e:
        logging.error(f'Error deleting image: {str(e)}')
        flash('An error occurred while deleting image.', 'error')
    
    return redirect(url_for('admin.images'))

@admin_bp.route('/messages')
@login_required
def messages():
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/messages/mark_read/<int:message_id>')
@login_required
def mark_message_read(message_id):
    try:
        message = ContactMessage.query.get_or_404(message_id)
        message.is_read = True
        db.session.commit()
        flash('Message marked as read.', 'success')
    except Exception as e:
        logging.error(f'Error marking message as read: {str(e)}')
        flash('An error occurred.', 'error')
    
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/delete/<int:message_id>')
@login_required
def delete_message(message_id):
    try:
        message = ContactMessage.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted successfully!', 'success')
    except Exception as e:
        logging.error(f'Error deleting message: {str(e)}')
        flash('An error occurred while deleting message.', 'error')
    
    return redirect(url_for('admin.messages'))

@admin_bp.route('/company-info')
@login_required
def company_info():
    company_data = {
        'hero_title': get_content('home', 'hero_title'),
        'hero_subtitle': get_content('home', 'hero_subtitle'),
        'hero_description': get_content('home', 'hero_description'),
        'about_title': get_content('about', 'title'),
        'about_description': get_content('about', 'description'),
        'mission': get_content('about', 'mission'),
        'vision': get_content('about', 'vision'),
        'founded_year': get_content('about', 'founded_year'),
        'team_size': get_content('about', 'team_size'),
        'experience': get_content('about', 'experience')
    }
    return render_template('admin/company_info.html', company_data=company_data)

@admin_bp.route('/telecom-settings')
@login_required
def telecom_settings():
    telecom_data = {
        'stats_suppliers': get_content('home', 'stats_countries'),
        'stats_calls': get_content('home', 'stats_calls'),
        'stats_established': get_content('home', 'stats_uptime'),
        'stats_uptime': get_content('home', 'stats_customers'),
        'contact_email': get_content('contact', 'email'),
        'contact_phone': get_content('contact', 'phone'),
        'contact_address': get_content('contact', 'address'),
        'contact_hours': get_content('contact', 'hours')
    }
    return render_template('admin/telecom_settings.html', telecom_data=telecom_data)

@admin_bp.route('/update-company-info', methods=['POST'])
@login_required
def update_company_info():
    try:
        set_content('home', 'hero_title', request.form.get('hero_title'))
        set_content('home', 'hero_subtitle', request.form.get('hero_subtitle'))
        set_content('home', 'hero_description', request.form.get('hero_description'))
        set_content('about', 'title', request.form.get('about_title'))
        set_content('about', 'description', request.form.get('about_description'))
        set_content('about', 'mission', request.form.get('mission'))
        set_content('about', 'vision', request.form.get('vision'))
        set_content('about', 'founded_year', request.form.get('founded_year'))
        set_content('about', 'team_size', request.form.get('team_size'))
        set_content('about', 'experience', request.form.get('experience'))
        
        flash('Company information updated successfully!', 'success')
    except Exception as e:
        logging.error(f'Error updating company info: {str(e)}')
        flash('An error occurred while updating company information.', 'error')
    
    return redirect(url_for('admin.company_info'))

@admin_bp.route('/update-telecom-settings', methods=['POST'])
@login_required
def update_telecom_settings():
    try:
        set_content('home', 'stats_countries', request.form.get('stats_suppliers'))
        set_content('home', 'stats_calls', request.form.get('stats_calls'))
        set_content('home', 'stats_uptime', request.form.get('stats_established'))
        set_content('home', 'stats_customers', request.form.get('stats_uptime'))
        set_content('contact', 'email', request.form.get('contact_email'))
        set_content('contact', 'phone', request.form.get('contact_phone'))
        set_content('contact', 'address', request.form.get('contact_address'))
        set_content('contact', 'hours', request.form.get('contact_hours'))
        
        flash('Telecom settings updated successfully!', 'success')
    except Exception as e:
        logging.error(f'Error updating telecom settings: {str(e)}')
        flash('An error occurred while updating telecom settings.', 'error')
    
    return redirect(url_for('admin.telecom_settings'))

@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/settings/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('admin.settings'))
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('admin.settings'))
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('admin.settings'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('admin.settings'))
        
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        
    except Exception as e:
        logging.error(f'Error changing password: {str(e)}')
        flash('An error occurred while changing password.', 'error')
    
    return redirect(url_for('admin.settings'))
