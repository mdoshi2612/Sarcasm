# Generated by Django 2.2 on 2021-03-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_player_bonus_level_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='address',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='department',
            field=models.CharField(choices=[('Aerospace Engineering', 'Aerospace Engineering'), ('Animation', 'Animation'), ('Application Software Centre', 'Application Software Centre'), ('Applied Geophysics', 'Applied Geophysics'), ('Applied Statistics and Informatics', 'Applied Statistics and Informatics'), ('Biomedical Engineering', 'Biomedical Engineering'), ('Biosciences and Bioengineering', 'Biosciences and Bioengineering'), ('Biotechnology', 'Biotechnology'), ('Centre for Aerospace Systems Design and Engineering', 'Centre for Aerospace Systems Design and Engineering'), ('Centre for Distance Engineering Education Programme', 'Centre for Distance Engineering Education Programme'), ('Centre for Environmental Science and Engineering', 'Centre for Environmental Science and Engineering'), ('Centre for Formal Design and Verification of Software', 'Centre for Formal Design and Verification of Software'), ('Centre for Research in Nanotechnology and Science', 'Centre for Research in Nanotechnology and Science'), ('Centre for Technology Alternatives for Rural Areas', 'Centre for Technology Alternatives for Rural Areas'), ('Centre for Urban Science and Engineering', 'Centre for Urban Science and Engineering'), ('Centre of Studies in Resources Engineering', 'Centre of Studies in Resources Engineering'), ('Chemical Engineering', 'Chemical Engineering'), ('Chemistry', 'Chemistry'), ('Civil Engineering', 'Civil Engineering'), ('Climate Studies', 'Climate Studies'), ('Computer Centre', 'Computer Centre'), ('Computer Science & Engineering', 'Computer Science & Engineering'), ('Continuing Education Programme', 'Continuing Education Programme'), ('Corrosion Science and Engineering', 'Corrosion Science and Engineering'), ('Desai Sethi Centre for Entrepreneurship', 'Desai Sethi Centre for Entrepreneurship'), ('Earth Sciences', 'Earth Sciences'), ('Educational Technology', 'Educational Technology'), ('Electrical Engineering', 'Electrical Engineering'), ('Energy Science and Engineering', 'Energy Science and Engineering'), ('Humanities & Social Science', 'Humanities & Social Science'), ('IITB-Monash Research Academy', 'IITB-Monash Research Academy'), ('Industrial Design Centre', 'Industrial Design Centre'), ('Industrial Design Centre', 'Industrial Design Centre'), ('Industrial Engineering and Operations Research', 'Industrial Engineering and Operations Research'), ('Industrial Management', 'Industrial Management'), ('Interaction Design', 'Interaction Design'), ('Kanwal Rekhi School of Information Technology', 'Kanwal Rekhi School of Information Technology'), ('Material Science', 'Material Science'), ('Materials, Manufacturing and Modelling', 'Materials, Manufacturing and Modelling'), ('Mathematics', 'Mathematics'), ('Mechanical Engineering', 'Mechanical Engineering'), ('Metallurgical Engineering & Materials Science', 'Metallurgical Engineering & Materials Science'), ('Mobility and Vehicle Design', 'Mobility and Vehicle Design'), ('National Centre for Aerospace Innovation and Research', 'National Centre for Aerospace Innovation and Research'), ('National Centre for Mathematics', 'National Centre for Mathematics'), ('Physical Education', 'Physical Education'), ('Physics', 'Physics'), ('Physics, Material Science', 'Physics, Material Science'), ('Preparatory Course', 'Preparatory Course'), ('Reliability Engineering', 'Reliability Engineering'), ('Shailesh J. Mehta School of Management', 'Shailesh J. Mehta School of Management'), ('Sophisticated Analytical Instrument Facility', 'Sophisticated Analytical Instrument Facility'), ('Systems and Control Engineering', 'Systems and Control Engineering'), ('Tata Center for Technology and Design', 'Tata Center for Technology and Design'), ('Technology and Development', 'Technology and Development'), ('Visual Communication', 'Visual Communication'), ('Wadhwani Research Centre for Bioengineering', 'Wadhwani Research Centre for Bioengineering')], default='Chemistry', max_length=255),
            preserve_default=False,
        ),
    ]
