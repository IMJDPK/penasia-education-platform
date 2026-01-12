#!/usr/bin/env python3
"""
Update course pricing to match January 2026 pricing structure
"""

import sqlite3

def update_pricing():
    """Update course pricing in the database"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), 'penasia.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update Hotel Culinary Management
    cursor.execute("""
        UPDATE course 
        SET fee_hkd = 125000 
        WHERE course_code = 'PSCE-DHM-5266'
    """)
    print("✓ Updated Hotel Culinary Management: HK$141,100 → HK$125,000")
    
    # Update BTEC Business Management
    cursor.execute("""
        UPDATE course 
        SET fee_hkd = 118000 
        WHERE course_code = 'PSCE-BTB-5001'
    """)
    print("✓ Updated BTEC Business Management: HK$78,000 → HK$118,000")
    
    # Verify updates
    cursor.execute("""
        SELECT course_code, title, fee_hkd 
        FROM course 
        WHERE is_active = 1
        ORDER BY id
    """)
    
    print("\n" + "="*70)
    print("Current Active Courses:")
    print("="*70)
    
    for row in cursor.fetchall():
        code, title, fee = row
        print(f"{code}: {title[:40]:40} HK${fee:,.0f}")
    
    conn.commit()
    conn.close()
    print("\n✓ Database updated successfully!")

if __name__ == '__main__':
    update_pricing()
