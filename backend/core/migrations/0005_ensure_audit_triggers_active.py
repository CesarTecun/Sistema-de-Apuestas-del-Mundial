from django.db import migrations


# SQL para recrear la función de auditoría y triggers
CREATE_AUDIT_FUNCTION_V2 = """
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
DECLARE
    pk_col text;
    pk_val text;
    old_json jsonb;
    new_json jsonb;
BEGIN
    -- Obtener nombre de la columna PK (usualmente 'id' o el primer campo)
    pk_col := TG_ARGV[0];

    IF (TG_OP = 'DELETE') THEN
        EXECUTE format('SELECT ($1).%I::text', pk_col) USING OLD INTO pk_val;
        old_json := to_jsonb(OLD);
        new_json := NULL;
        INSERT INTO audit_log (table_name, operation, record_pk, old_data, new_data, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, 'DELETE', pk_val, old_json, new_json, CURRENT_USER, NOW());
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        EXECUTE format('SELECT ($1).%I::text', pk_col) USING NEW INTO pk_val;
        old_json := to_jsonb(OLD);
        new_json := to_jsonb(NEW);
        INSERT INTO audit_log (table_name, operation, record_pk, old_data, new_data, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, 'UPDATE', pk_val, old_json, new_json, CURRENT_USER, NOW());
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        EXECUTE format('SELECT ($1).%I::text', pk_col) USING NEW INTO pk_val;
        old_json := NULL;
        new_json := to_jsonb(NEW);
        INSERT INTO audit_log (table_name, operation, record_pk, old_data, new_data, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, 'INSERT', pk_val, old_json, new_json, CURRENT_USER, NOW());
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""

DROP_TRIGGERS_SQL = """
DROP TRIGGER IF EXISTS audit_usuario ON usuario;
DROP TRIGGER IF EXISTS audit_liga ON liga;
DROP TRIGGER IF EXISTS audit_pronostico ON pronostico;
DROP TRIGGER IF EXISTS audit_partido ON partido;
DROP TRIGGER IF EXISTS audit_participanteliga ON participante_liga;
"""

CREATE_TRIGGERS_SQL = """
CREATE TRIGGER audit_usuario
    AFTER INSERT OR UPDATE OR DELETE ON usuario
    FOR EACH ROW EXECUTE FUNCTION audit_trigger('id_usuario');

CREATE TRIGGER audit_liga
    AFTER INSERT OR UPDATE OR DELETE ON liga
    FOR EACH ROW EXECUTE FUNCTION audit_trigger('id_liga');

CREATE TRIGGER audit_pronostico
    AFTER INSERT OR UPDATE OR DELETE ON pronostico
    FOR EACH ROW EXECUTE FUNCTION audit_trigger('id_pronostico');

CREATE TRIGGER audit_partido
    AFTER INSERT OR UPDATE OR DELETE ON partido
    FOR EACH ROW EXECUTE FUNCTION audit_trigger('id_partido');

CREATE TRIGGER audit_participanteliga
    AFTER INSERT OR UPDATE OR DELETE ON participante_liga
    FOR EACH ROW EXECUTE FUNCTION audit_trigger('id_participante');
"""


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_audit_triggers'),
        ('ligas', '0009_add_audit_fields_to_liga'),
    ]

    operations = [
        migrations.RunSQL(
            sql=DROP_TRIGGERS_SQL + CREATE_AUDIT_FUNCTION_V2 + CREATE_TRIGGERS_SQL,
            reverse_sql=DROP_TRIGGERS_SQL,
        ),
    ]
