"""Seed instances into the database"""
from app.database import SessionLocal
from app import models

db = SessionLocal()

instances_to_add = [
    {
        "name": "EC2 Production",
        "instance_id": "i-0347ad6ae12bdb460",
        "ip_address": "13.201.66.26",
        "port": 9100,
        "region": "ap-south-1",
        "instance_type": "t2.micro",
        "status": "active",
        "is_monitored": True,
        "owner_id": 1,
    },
    {
        "name": "Local Node",
        "instance_id": "node-exporter",
        "ip_address": "node-exporter",
        "port": 9100,
        "region": "local",
        "instance_type": "local",
        "status": "active",
        "is_monitored": True,
        "owner_id": 1,
    },
]

added = 0
for inst_data in instances_to_add:
    existing = db.query(models.Instance).filter(
        models.Instance.instance_id == inst_data["instance_id"]
    ).first()
    if not existing:
        instance = models.Instance(**inst_data)
        db.add(instance)
        added += 1
        print(f"  Added: {inst_data['name']} ({inst_data['instance_id']})")
    else:
        print(f"  Skipped (already exists): {inst_data['instance_id']}")

db.commit()
db.close()
print(f"\nDone! Added {added} instance(s).")
