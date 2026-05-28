from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("autenticacion", "0003_sesionusuario_jwt_jti_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS token_blacklist_blacklistedtoken CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS token_blacklist_outstandingtoken CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
