import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
django.setup()

from home.models import Profile, Project, Skill, Testimonial

def create_initial_data():
    # Créer le profil
    profile, created = Profile.objects.get_or_create(
        pk=1,
        defaults={
            'full_name': 'DELAMOU Samaké',
            'title': 'Data Analyst',
            'bio': 'Passionné par l\'analyse de données et l\'extraction d\'insights pertinents pour aider les entreprises à prendre des décisions éclairées.',
            'profile_image': 'delamou.jpg',
            'email': 'samakedelamou858@gmail.com',
            'phone': '+223 629403019',
            'location': 'Conakry, Guinée',
            'linkedin': 'https://linkedin.com/in/delamou-samake',
            'github': 'https://github.com/Delamou1234',
            'twitter': 'https://twitter.com/delamou_samake',
            'kaggle': 'https://kaggle.com/delamousamake',
            'years_experience': 3,
            'projects_count': 50,
            'clients_count': 15,
        }
    )
    
    # Créer les compétences
    skills_data = [
        # Analyse de données
        ('Statistiques descriptives', 'analysis', 'fas fa-chart-line'),
        ('Analyse exploratoire', 'analysis', 'fas fa-search'),
        ('Data cleaning', 'analysis', 'fas fa-broom'),
        ('Feature engineering', 'analysis', 'fas fa-cogs'),
        
        # Programmation
        ('Python (Pandas, NumPy, Matplotlib)', 'programming', 'fas fa-code'),
        ('SQL', 'programming', 'fas fa-database'),
        ('R', 'programming', 'fab fa-r-project'),
        ('JavaScript (D3.js)', 'programming', 'fab fa-js'),
        
        # Bases de données
        ('MySQL', 'database', 'fas fa-database'),
        ('PostgreSQL', 'database', 'fas fa-database'),
        ('MongoDB', 'database', 'fas fa-leaf'),
        ('BigQuery', 'database', 'fas fa-cloud'),
        
        # Business Intelligence
        ('Tableau', 'bi', 'fas fa-chart-pie'),
        ('Power BI', 'bi', 'fas fa-chart-bar'),
        ('Looker Studio', 'bi', 'fas fa-chart-line'),
        ('Excel avancé', 'bi', 'fas fa-file-excel'),
    ]
    
    for name, category, icon in skills_data:
        Skill.objects.get_or_create(
            name=name,
            category=category,
            defaults={'icon': icon}
        )
    
    # Créer les projets
    projects_data = [
        {
            'title': 'Dashboard de ventes interactif',
            'description': 'Création d\'un dashboard dynamique pour suivre les performances de ventes en temps réel avec Tableau.',
            'image': 'placeholder.svg',
            'technologies': 'Tableau, SQL, Python',
            'featured': True,
        },
        {
            'title': 'Segmentation client RFM',
            'description': 'Analyse comportementale des clients et segmentation RFM pour optimiser les campagnes marketing.',
            'image': 'placeholder.svg',
            'technologies': 'Python, Pandas, Scikit-learn',
            'featured': True,
        },
        {
            'title': 'Prévision de la demande',
            'description': 'Modèle de prévision de la demande pour optimiser la gestion des stocks et réduire les coûts.',
            'image': 'placeholder.svg',
            'technologies': 'Python, Time Series, Machine Learning',
            'featured': True,
        },
        {
            'title': 'Analyse des sentiments clients',
            'description': 'Analyse des commentaires clients pour améliorer la satisfaction et identifier les tendances.',
            'image': 'placeholder.svg',
            'technologies': 'Python, NLP, Text Mining',
            'featured': False,
        },
        {
            'title': 'Optimisation des prix',
            'description': 'Modèle d\'optimisation des prix basé sur l\'élasticité de la demande et la concurrence.',
            'image': 'placeholder.svg',
            'technologies': 'Python, Machine Learning, Optimization',
            'featured': False,
        },
        {
            'title': 'Tableau de bord KPI',
            'description': 'Développement d\'un tableau de bord complet pour suivre les indicateurs de performance clés.',
            'image': 'placeholder.svg',
            'technologies': 'Power BI, SQL, Excel',
            'featured': False,
        },
    ]
    
    for project_data in projects_data:
        Project.objects.get_or_create(
            title=project_data['title'],
            defaults=project_data
        )
    
    # Créer les témoignages
    testimonials_data = [
        {
            'client_name': 'Marie Konaté',
            'client_company': 'Tech Solutions SA',
            'message': 'DELAMOU a transformé nos données brutes en insights actionnables. Son travail sur notre dashboard de ventes a considérablement amélioré notre prise de décision.',
            'rating': 5,
            'featured': True,
        },
        {
            'client_name': 'Brahima Touré',
            'client_company': 'Retail Group',
            'message': 'Expert en analyse de données, DELAMOU nous a aidés à optimiser notre inventaire et à réduire nos coûts de 20%. Je recommande vivement.',
            'rating': 5,
            'featured': True,
        },
        {
            'client_name': 'Aminata Diarra',
            'client_company': 'Marketing Pro',
            'message': 'La segmentation client RFM réalisée par DELAMOU a transformé nos campagnes marketing. Excellent professionnel et très réactif.',
            'rating': 5,
            'featured': True,
        },
    ]
    
    for testimonial_data in testimonials_data:
        Testimonial.objects.get_or_create(
            client_name=testimonial_data['client_name'],
            defaults=testimonial_data
        )
    
    print("Données initiales créées avec succès!")

if __name__ == '__main__':
    create_initial_data()
