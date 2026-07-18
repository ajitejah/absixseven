from django.core.management.base import BaseCommand

from app_setting.models import Setting


class Command(BaseCommand):
    help = "Seed default application settings"

    def handle(self, *args, **kwargs):

        # Reset semua setting
        self.stdout.write("Deleting old settings...")
        Setting.objects.all().delete()

        settings = [

            ("WEB", "SEO", "site_name", "Nama Website",
            "IBSIXSEVEN", "text"),

            ("WEB", "SEO", "meta_title", "Meta Title",
            "IBSIXSEVEN | Platform Roadmap Pembelajaran", "text"),

            ("WEB", "SEO", "meta_description", "Meta Description",
            "...", "textarea"),

            ("WEB", "SEO", "meta_keywords", "Meta Keywords",
            "...", "textarea"),

            ("WEB", "SEO", "meta_author", "Meta Author",
            "IBSIXSEVEN", "text"),

            ("WEB", "SEO", "meta_robots", "Meta Robots",
            "index, follow", "text"),

            ("WEB", "SEO", "canonical_url", "Canonical URL",
            "https://ibsixseven.com", "text"),

            ("WEB", "BRANDING", "logo_light", "Logo Terang",
            "setting/web/logo_6s2imeP.png", "image"),

            ("WEB", "BRANDING", "logo_dark", "Logo Gelap",
            "setting/web/logo.png", "image"),

            ("WEB", "BRANDING", "favicon", "Favicon",
            "setting/web/logo_wCunQUc.png", "image"),

            ("WEB", "BRANDING", "og_image", "Open Graph Image",
            "", "image"),

            ("WEB", "BRANDING", "twitter_image", "Twitter Image",
            "", "image"),

            ("WEB", "BRANDING", "og_title", "Open Graph Title",
            "", "text"),

            ("WEB", "BRANDING", "og_description", "Open Graph Description",
            "", "textarea"),

            ("WEB", "BRANDING", "twitter_title", "Twitter Title",
            "", "text"),

            ("WEB", "BRANDING", "twitter_description", "Twitter Description",
            "", "textarea"),

            ("WEB", "CONTACT", "short_description", "Deskripsi Singkat",
            "...", "textarea"),

            ("WEB", "CONTACT", "address", "Alamat",
            "...", "textarea"),

            ("WEB", "CONTACT", "email", "Email",
            "...", "text"),

            ("WEB", "CONTACT", "phone", "Telepon",
            "...", "text"),

            ("WEB", "CONTACT", "whatsapp", "WhatsApp",
            "...", "text"),

            ("WEB", "SOCIAL", "instagram", "Instagram",
            "...", "text"),

            ("WEB", "SOCIAL", "facebook", "Facebook",
            "...", "text"),

            ("WEB", "SOCIAL", "youtube", "YouTube",
            "...", "text"),

            ("WEB", "SOCIAL", "linkedin", "LinkedIn",
            "...", "text"),

            ("WEB", "SOCIAL", "tiktok", "TikTok",
            "...", "text"),

            ("WEB", "ANALYTICS", "google_analytics", "Google Analytics ID",
            "", "text"),

            ("WEB", "ANALYTICS", "google_tag_manager", "Google Tag Manager ID",
            "", "text"),

            ("WEB", "ANALYTICS", "copyright", "Copyright",
            "© IBSIXSEVEN. All rights reserved.", "text"),

            ############################################################
            # HEADER
            ############################################################

            ("CONTENT", "HEADER", "title", "Judul Header",
             "Belajar Lebih Terarah Bersama IBSIXSEVEN", "text"),

            ("CONTENT", "HEADER", "subtitle", "Sub Judul Header",
             "Platform pembelajaran yang menghubungkan siswa, guru, dan orang tua melalui roadmap pembelajaran yang terstruktur.", "textarea"),

            ("CONTENT", "HEADER", "image", "Gambar Header",
             "", "image"),

            ############################################################
            # THREE ICON
            ############################################################

            ("CONTENT", "ICON1", "icon", "Icon 1",
             "heroicons:map", "icon"),

            ("CONTENT", "ICON1", "title", "Judul Icon 1",
             "Roadmap Manager", "text"),

            ("CONTENT", "ICON1", "subtitle", "Sub Judul Icon 1",
             "Roadmap pembelajaran yang sistematis mulai dari checkpoint hingga submission tugas.", "textarea"),

            ("CONTENT", "ICON2", "icon", "Icon 2",
             "heroicons:chart-bar-square", "icon"),

            ("CONTENT", "ICON2", "title", "Judul Icon 2",
             "Evaluasi", "text"),

            ("CONTENT", "ICON2", "subtitle", "Sub Judul Icon 2",
             "Pantau perkembangan siswa melalui grafik dan laporan hasil belajar.", "textarea"),

            ("CONTENT", "ICON3", "icon", "Icon 3",
             "heroicons:rocket-launch", "icon"),

            ("CONTENT", "ICON3", "title", "Judul Icon 3",
             "Proyeksi", "text"),

            ("CONTENT", "ICON3", "subtitle", "Sub Judul Icon 3",
             "Prediksi kesiapan siswa menuju institusi pendidikan internasional.", "textarea"),

            ############################################################
            # ROADMAP
            ############################################################

            ("CONTENT", "ROADMAP", "cover", "Cover",
             "media/setting/compro/cover-animate-lp-1.jpg", "image"),

            ("CONTENT", "ROADMAP", "video", "Video Hover",
             "media/setting/compro/cover-animate-lp-1.jpg", "video"),

            ("CONTENT", "ROADMAP", "title", "Judul",
             "Roadmap Manager", "text"),

            ("CONTENT", "ROADMAP", "subtitle", "Sub Judul",
             "Kelola roadmap pembelajaran secara terstruktur.", "textarea"),

            ("CONTENT", "ROADMAP", "description", "Deskripsi",
             "Menyusun proses pembelajaran secara terstruktur melalui roadmap yang terdiri atas beberapa checkpoint dan tugas. Siswa mengirimkan submission pada setiap tugas, kemudian guru memberikan penilaian dan umpan balik.", "textarea"),

            ############################################################
            # EVALUATION
            ############################################################

            ("CONTENT", "EVALUATION", "cover", "Cover",
             "media/setting/compro/cover-animate-lp-2.jpg", "image"),

            ("CONTENT", "EVALUATION", "video", "Video Hover",
             "media/setting/compro/cover-animate-lp-2.jpg", "video"),

            ("CONTENT", "EVALUATION", "title", "Judul",
             "Evaluasi", "text"),

            ("CONTENT", "EVALUATION", "subtitle", "Sub Judul",
             "Pantau perkembangan belajar melalui grafik.", "textarea"),

            ("CONTENT", "EVALUATION", "description", "Deskripsi",
             "Menampilkan perkembangan belajar siswa berdasarkan roadmap yang dikerjakan, lengkap dengan hasil penilaian dan visualisasi grafik untuk memudahkan pemantauan kemajuan.", "textarea"),

            ############################################################
            # PROJECTION
            ############################################################

            ("CONTENT", "PROJECTION", "cover", "Cover",
             "media/setting/compro/cover-animate-lp-3.jpg", "image"),

            ("CONTENT", "PROJECTION", "video", "Video Hover",
             "media/setting/compro/cover-animate-lp-3.jpg", "video"),

            ("CONTENT", "PROJECTION", "title", "Judul",
             "Proyeksi", "text"),

            ("CONTENT", "PROJECTION", "subtitle", "Sub Judul",
             "Prediksi kesiapan siswa menuju target belajar.", "textarea"),

            ("CONTENT", "PROJECTION", "description", "Deskripsi",
             "Menganalisis hasil pembelajaran siswa untuk memproyeksikan tingkat kesiapan menghadapi ujian atau sertifikasi pada institusi internasional berdasarkan capaian roadmap.", "textarea"),

        ]

        for order, (
            group,
            section,
            key,
            label,
            value,
            setting_type,
        ) in enumerate(settings, start=1):

            defaults = {
                "label": label,
                "type": setting_type,
                "order": order,
                "is_active": True,
            }

            # Simpan sesuai tipe field
            if setting_type == "image":
                defaults["image"] = value
            elif setting_type == "video":
                defaults["video"] = value
            else:
                defaults["value"] = value

            Setting.objects.update_or_create(
                group=group,
                section=section,
                key=key,
                defaults=defaults,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ {len(settings)} default settings have been seeded successfully."
            )
        )