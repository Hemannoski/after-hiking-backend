from django.urls import path

from .views import FirebaseLoginView, PhotoProfilView, MoiView, ProfilUtilisateurView, RechercheUtilisateursView

urlpatterns = [
    path('auth/firebase', FirebaseLoginView.as_view(), name='auth-firebase'),
    path('moi/photo', PhotoProfilView.as_view(), name='moi-photo'),
    path('moi', MoiView.as_view(), name='moi'),
    path('utilisateurs/<int:pk>', ProfilUtilisateurView.as_view(), name='utilisateur-profil'),
    path('recherche/utilisateurs', RechercheUtilisateursView.as_view(), name='recherche-utilisateurs'),
]