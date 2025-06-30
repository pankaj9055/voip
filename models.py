from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(20), default='text')  # text, html, image_url
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('section', 'key', name='_section_key_uc'),)

class CarouselImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def get_content(section, key, default=''):
    content = Content.query.filter_by(section=section, key=key).first()
    return content.value if content else default

def set_content(section, key, value, content_type='text'):
    content = Content.query.filter_by(section=section, key=key).first()
    if content:
        content.value = value
        content.content_type = content_type
        content.updated_at = datetime.utcnow()
    else:
        content = Content()
        content.section = section
        content.key = key
        content.value = value
        content.content_type = content_type
        db.session.add(content)
    db.session.commit()

def create_default_data():
    # Create default admin user
    if not Admin.query.first():
        admin = Admin()
        admin.username = 'admin'
        admin.email = 'admin@voipfit.com'
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create default content
    default_content = {
        'home': {
            'hero_title': 'Turn product ideas into concepts instantly with VoipFit',
            'hero_subtitle': 'Visualize, communicate, and iterate on telecom solutions in minutes. Empower your business with premium VoIP services!',
            'hero_description': 'Premium VoIP services for businesses worldwide. Connect, communicate, and grow with VoipFit - your trusted telecom partner since 2018.',
            'stats_countries': '150+',
            'stats_calls': '5M+',
            'stats_uptime': '99.9%',
            'stats_customers': '10K+'
        },
        'about': {
            'title': 'About VoipFit',
            'description': 'VoipFit is a leading telecommunications company founded in 2018, providing premium VoIP services to businesses across 150+ countries. We handle over 5 million calls daily with 99.9% uptime guarantee.',
            'mission': 'To revolutionize business communications through innovative VoIP solutions and exceptional customer service.',
            'vision': 'To be the global leader in telecommunications, connecting businesses worldwide with reliable, affordable, and feature-rich communication solutions.',
            'founded_year': '2018',
            'team_size': '500+',
            'experience': '6+ Years'
        },
        'services': {
            'title': 'Our Services',
            'description': 'Comprehensive VoIP solutions tailored for your business needs',
            'service1_title': 'Business VoIP',
            'service1_desc': 'Advanced VoIP solutions for businesses of all sizes with premium call quality and reliability.',
            'service2_title': 'Call Service',
            'service2_desc': 'Professional call management services with advanced routing and quality assurance.',
            'service3_title': 'Message Service',
            'service3_desc': 'Integrated messaging solutions for business communications and customer engagement.',
            'service4_title': 'Call Center Solutions',
            'service4_desc': 'Complete call center solutions with analytics, reporting, and automation tools.',
            'service5_title': 'Mobile VoIP',
            'service5_desc': 'Mobile applications for VoIP calling with HD voice quality and global coverage.',
            'service6_title': '24/7 Support',
            'service6_desc': 'Round-the-clock technical support and customer service from our expert team.'
        },
        'contact': {
            'title': 'Contact Us',
            'description': 'Get in touch with our team for any inquiries or support needs',
            'address': '123 Tech Plaza, Digital District, San Francisco, CA 94105',
            'phone': '+1 (555) 123-4567',
            'email': 'info@voipfit.com',
            'hours': 'Mon-Fri: 9AM-6PM PST'
        },
        'footer': {
            'description': 'Premium VoIP solutions for businesses worldwide. Connecting the future of communication since 2018.',
            'copyright': '© 2024 VoipFit. All rights reserved.',
            'powered_by': 'Powering 150+ countries with premium VoIP',
            'footer_email': 'info@voipfit.com',
            'footer_phone': '+1 (555) 123-4567',
            'footer_location': 'San Francisco, CA'
        },
        'features': {
            'section_title': 'Why Choose VoipFit?',
            'section_subtitle': 'Experience the future of business communication',
            'feature1_title': 'Lightning Fast',
            'feature1_desc': 'Ultra-low latency connections with crystal clear voice quality across all networks.',
            'feature2_title': 'Enterprise Security',
            'feature2_desc': 'Bank-level encryption and security protocols to protect your business communications.',
            'feature3_title': 'Scalable Solutions',
            'feature3_desc': 'Grow your communication infrastructure seamlessly with our flexible VoIP solutions.',
            'feature4_title': '24/7 Support',
            'feature4_desc': 'Round-the-clock technical support from our team of VoIP experts and specialists.',
            'feature5_title': 'Advanced Analytics',
            'feature5_desc': 'Comprehensive reporting and analytics to optimize your communication performance.',
            'feature6_title': 'Cost Effective',
            'feature6_desc': 'Reduce your communication costs by up to 60% with our competitive pricing plans.'
        },
        'cta': {
            'title': 'Ready to Transform Your Business Communication?',
            'subtitle': 'Join thousands of businesses worldwide who trust VoipFit for their communication needs.'
        }
    }
    
    for section, content_dict in default_content.items():
        for key, value in content_dict.items():
            if not Content.query.filter_by(section=section, key=key).first():
                content = Content()
                content.section = section
                content.key = key
                content.value = value
                db.session.add(content)
    
    # Create default carousel images
    if not CarouselImage.query.first():
        carousel_images = [
            {'title': 'Business VoIP Solutions', 'image_url': 'https://pixabay.com/get/g88d2a236c42231c26d40cff6937c30315e8204e32bf3f824a5e4eebca49e9402df6ebb8b6f65632766c3f4ef826aa7b64d2a67ebb6338b69a3c6d4c503bc4a28_1280.jpg', 'order_index': 1},
            {'title': 'Call Service Solutions', 'image_url': 'https://pixabay.com/get/g8d395aa18d84819e7e8f683cd76c56078a923c0c87f9aa9a27ec6f735dfac972583258e34eb4b795ec6c8d8e3313e7daa7eddc37c138ac2939a34fb37d7fd6ac_1280.jpg', 'order_index': 2},
            {'title': 'Message Service Technology', 'image_url': 'https://pixabay.com/get/g0c22dcf3b4f9da724dfa5645f9f05ec03338a37470dd7ec35939755870a3401d2bbae37f59021da1f600c27583c7e1a2dc66c8e1630005ad9df23506c0ccc37c_1280.jpg', 'order_index': 3},
            {'title': 'Global Network Connectivity', 'image_url': 'https://pixabay.com/get/g6414634b30e4b630124901e4c2c0395f147e50cf3421add50cabf84f2ec796c069b8500d7674171a93294383b25fd68c0471f1f4ca06efe84c6eef84ac3b602f_1280.jpg', 'order_index': 4},
            {'title': 'Professional Communication', 'image_url': 'https://pixabay.com/get/g5912fde8be90ae1e8725d21062fdb58200579e11b2da21e884426e7f4150f6757d57209779cb1f016ed75b877a5957edc5ea28d6e97b7e6b2c1108852fbc0632_1280.jpg', 'order_index': 5},
            {'title': 'Innovation & Support', 'image_url': 'https://pixabay.com/get/g38f467ceb783e10c5eeb1e9e6f88da20026565e105f1153c13b80ca5383122b9f8998c71d06f819d69cdce64c2ecbb58278a5b4841aad5d34e6bb5f39a44c307_1280.jpg', 'order_index': 6}
        ]
        
        for img_data in carousel_images:
            image = CarouselImage(**img_data)
            db.session.add(image)
    
    db.session.commit()
