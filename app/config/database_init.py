import logging
from datetime import datetime, timezone
from pony.orm import db_session, Database
from app.models.department import Department
from app.models.role import Role
from app.models.permission import Permission
from app.models.division import Division

logger = logging.getLogger(__name__)

def init_database(db: Database):
    with db_session:
        divisions_data = [
            {"name": "Divisi Keuangan", "color": "#9b59b6", "code": "VKU", "type": "Divisi"},
            {"name": "Divisi Pendidikan", "color": "#1981cc", "code": "VPD", "type": "Divisi"},
            {"name": "Divisi Penstra", "color": "#e74c3c", "code": "VPS", "type": "Divisi"},
            {"name": "Divisi SDM", "color": "#00bfff", "code": "VSM", "type": "Divisi"},
            {"name": "Divisi Sarpras", "color": "#f1c40f", "code": "VSR", "type": "Divisi"},
            {"name": "Divisi SIM A", "color": "#B07E9F", "code": "VSI", "type": "Divisi"},
            {"name": "Biro Kerohanian", "color": "#9b59b6", "code": "BKR", "type": "Biro"},
            {"name": "Biro Sekretariat Korporasi", "color": "#3498db", "code": "BSK", "type": "Biro"},
            {"name": "Biro PKK", "color": "#e74c3c", "code": "BKK", "type": "Biro"},
        ]
        
        for div_data in divisions_data:
            Division(**div_data)

        # Get division references
        div_sdm = Division.get(code="VSM")
        div_pendidikan = Division.get(code="VPD")
        div_penstra = Division.get(code="VPS")
        div_sarpras = Division.get(code="VSR")
        div_sim = Division.get(code="VSI")

        departments_data = [
            # VSM Division
            {"name": "Bagian Keuangan", "code": "BKU", "division": div_sdm, "color": "#FF9F9F"},
            {"name": "Bagian Akunting", "code": "BAP", "division": div_sdm, "color": "#FFB8B8"},
            
            # VPD Division
            {"name": "Kepala Jenjang International", "code": "JIT", "division": div_pendidikan, "color": "#9FD4FF"},
            
            # Pendidikan Division
            {"name": "Kepala Jenjang TK", "code": "JTK", "division": div_pendidikan, "color": "#B8DCFF"},
            {"name": "Kepala Jenjang SD", "code": "JSD", "division": div_pendidikan, "color": "#C8E3FF"},
            {"name": "Kepala Jenjang SMP", "code": "JMP", "division": div_pendidikan, "color": "#D8EAFF"},
            {"name": "Kepala Jenjang SLTA", "code": "JMA", "division": div_pendidikan, "color": "#E8F1FF"},
            {"name": "Layanan dan Pendukung Pendidikan", "code": "BLP", "division": div_pendidikan, "color": "#F0F5FF"},
            {"name": "Kurikulum dan Evaluasi", "code": "BKE", "division": div_pendidikan, "color": "#F8FAFF"},
            
            # Penstra Division
            {"name": "Bagian Komunikasi, Pemasaran, dan Penerimaan Siswa Baru", "code": "BPP", "division": div_penstra, "color": "#FF9F9F"},
            {"name": "Bagian Riset dan Pengembangan", "code": "BRP", "division": div_penstra, "color": "#FFB8B8"},
            {"name": "Bagian Pengendalian Mutu", "code": "BPM", "division": div_penstra, "color": "#FFC8C8"},
            
            # SDM Division
            {"name": "Bagian Pengembangan SDM, Organisasi, dan Sistem SDM", "code": "BPO", "division": div_sdm, "color": "#FFC8C8"},
            {"name": "Bagian Penyediaan, Personalia, dan Kesejahteraan SDM", "code": "BPR", "division": div_sdm, "color": "#FFD8D8"},
            
            # Sarpras Division
            {"name": "Bagian Pengadaan", "code": "BPD", "division": div_sarpras, "color": "#FFE59F"},
            {"name": "Bagian Pembangunan", "code": "BPB", "division": div_sarpras, "color": "#FFEBB8"},
            {"name": "Bagian Manajemen Gedung", "code": "BMG", "division": div_sarpras, "color": "#FFF0C8"},
            
            # SIM Division
            {"name": "Bagian Jaringan Infrastruktur", "code": "BJI", "division": div_sim, "color": "#E5B8FF"},
            {"name": "Bagian Layanan Teknologi Informasi", "code": "BTI", "division": div_sim, "color": "#ECC8FF"},
            {"name": "Bagian Pengembangan Sistem dan Aplikasi", "code": "BPA", "division": div_sim, "color": "#F2D8FF"},
        ]
                
        for dept_data in departments_data:
            Department(**dept_data)

        # Initialize Permissions
        permissions_data = [
            {"name": "Manage Roles", "action": "manage", "subject": "roles"},
            {"name": "Manage Master Data", "action": "manage", "subject": "master_data"},
            {"name": "View All Calendars", "action": "view", "subject": "all_calendars"},
            {"name": "Edit All Calendars", "action": "edit", "subject": "all_calendars"},
            {"name": "Delete All Calendars", "action": "delete", "subject": "all_calendars"},
            {"name": "View Division Calendars", "action": "view", "subject": "division_calendars"},
            {"name": "Edit Division Calendars", "action": "edit", "subject": "division_calendars"},
            {"name": "Delete Division Calendars", "action": "delete", "subject": "division_calendars"},
            {"name": "View Department Calendars", "action": "view", "subject": "department_calendars"},
            {"name": "Edit Department Calendars", "action": "edit", "subject": "department_calendars"},
            {"name": "Delete Department Calendars", "action": "delete", "subject": "department_calendars"},
            {"name": "View User Calendars", "action": "view", "subject": "user_calendars"},
        ]
        
        created_permissions = {}
        for perm_data in permissions_data:
            perm = Permission(**perm_data)
            created_permissions[f"{perm_data['action']}_{perm_data['subject']}"] = perm

        # Initialize Roles with Permissions
        roles_data = [
            {
                "name": "Super Admin",
                "permissions": [
                    "manage_roles", "manage_master_data",
                    "view_all_calendars", "edit_all_calendars", "delete_all_calendars"
                ]
            },
            {
                "name": "Admin Global",
                "permissions": [
                    "view_all_calendars", "edit_all_calendars", "delete_all_calendars"
                ]
            },
            {
                "name": "Tim9",
                "permissions": ["view_all_calendars"]
            },
            {
                "name": "Admin Division",
                "permissions": [
                    "view_division_calendars", "edit_division_calendars", "delete_division_calendars",
                    "view_department_calendars", "edit_department_calendars", "delete_department_calendars"
                ]
            },
            {
                "name": "Admin Department",
                "permissions": [
                    "view_department_calendars", "edit_department_calendars", "delete_department_calendars"
                ]
            },
            {
                "name": "User",
                "permissions": ["view_user_calendars"]
            }
        ]

        for role_data in roles_data:
            role = Role(name=role_data["name"])
            for perm_key in role_data["permissions"]:
                perm = created_permissions.get(perm_key)
                if perm:
                    role.permissions.add(perm)

def reset_database(db: Database):
    logger.info("Starting database reset")
    
    try:
        with db_session:
            # Soft delete all existing records
            Department.select().delete(bulk=True)
            Division.select().delete(bulk=True)
            Permission.select().delete(bulk=True)
            Role.select().delete(bulk=True)
            
            logger.info("Existing data cleared")
            
        # Reinitialize with fresh data
        init_database(db)
        logger.info("Database reset completed successfully")
        
    except Exception as e:
        logger.error(f"Error during database reset: {str(e)}")
        raise