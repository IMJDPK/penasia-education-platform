#!/bin/bash
# PythonAnywhere Quick Deployment Script
# Run this on PythonAnywhere after git pull

echo "========================================"
echo "PenAsia Course Fix - Deployment Script"
echo "========================================"
echo ""

# Step 1: Check current directory
echo "📁 Current directory: $(pwd)"
if [[ $(pwd) != *"penasia-education-platform"* ]]; then
    echo "⚠️  WARNING: Not in penasia-education-platform directory!"
    echo "   Please run: cd ~/penasia-education-platform"
    exit 1
fi

# Step 2: Verify image files
echo ""
echo "📷 Checking course images..."
IMAGE_DIR="static/images/four courses images"
if [ -d "$IMAGE_DIR" ]; then
    echo "✅ Image directory exists"
    ls -lh "$IMAGE_DIR"
    
    # Check individual files
    if [ -f "$IMAGE_DIR/hotel_culinary.jpg" ]; then
        echo "  ✅ hotel_culinary.jpg found"
    else
        echo "  ❌ hotel_culinary.jpg MISSING!"
    fi
    
    if [ -f "$IMAGE_DIR/Btec.jpg" ]; then
        echo "  ✅ Btec.jpg found"
    else
        echo "  ❌ Btec.jpg MISSING!"
    fi
    
    if [ -f "$IMAGE_DIR/western-bakery.png" ]; then
        echo "  ✅ western-bakery.png found"
    else
        echo "  ❌ western-bakery.png MISSING!"
    fi
    
    if [ -f "$IMAGE_DIR/wester_cuisine.png" ]; then
        echo "  ✅ wester_cuisine.png found"
    else
        echo "  ❌ wester_cuisine.png MISSING!"
    fi
else
    echo "❌ Image directory NOT FOUND: $IMAGE_DIR"
    echo "   You need to create this folder and upload images!"
    exit 1
fi

# Step 3: Verify template
echo ""
echo "📄 Checking courses.html template..."
if grep -q "four courses images" templates/courses.html; then
    echo "✅ Template has correct image paths"
else
    echo "❌ Template does NOT have correct image paths!"
    echo "   Run: git pull origin main"
    exit 1
fi

# Step 4: Update database
echo ""
echo "💾 Updating database..."
if [ -f "update_courses.py" ]; then
    python3 update_courses.py
    if [ $? -eq 0 ]; then
        echo "✅ Database updated successfully"
    else
        echo "❌ Database update FAILED!"
        echo "   Check error messages above"
        exit 1
    fi
else
    echo "❌ update_courses.py not found!"
    echo "   Run: git pull origin main"
    exit 1
fi

# Step 5: Verify database changes
echo ""
echo "🔍 Verifying database..."
python3 << EOF
from app import app, db, Course

with app.app_context():
    courses = Course.query.order_by(Course.id).all()
    print("\n📊 Course Pricing Status:")
    print("-" * 70)
    for course in courses:
        status = "✓" if course.is_active else "✗"
        print(f"{status} ID {course.id:3d}: {course.title:40s} HK\${float(course.fee_hkd):>10,.0f}")
    print("-" * 70)
    
    # Check specific prices
    c169 = Course.query.get(169)
    c1 = Course.query.get(1)
    c171 = Course.query.get(171)
    c179 = Course.query.get(179)
    
    errors = []
    if c169 and float(c169.fee_hkd) != 125000:
        errors.append(f"Course 169 fee is {c169.fee_hkd}, should be 125000")
    if c1 and float(c1.fee_hkd) != 118000:
        errors.append(f"Course 1 fee is {c1.fee_hkd}, should be 118000")
    if c171 and float(c171.fee_hkd) != 12620:
        errors.append(f"Course 171 fee is {c171.fee_hkd}, should be 12620")
    if c179 and float(c179.fee_hkd) != 13200:
        errors.append(f"Course 179 fee is {c179.fee_hkd}, should be 13200")
    
    if errors:
        print("\n❌ PRICE ERRORS DETECTED:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("\n✅ All prices are correct!")
EOF

if [ $? -ne 0 ]; then
    echo "❌ Database verification failed!"
    exit 1
fi

# Step 6: Touch WSGI file to reload
echo ""
echo "🔄 Reloading web app..."
WSGI_FILE="/var/www/imjdpk_pythonanywhere_com_wsgi.py"
if [ -f "$WSGI_FILE" ]; then
    touch "$WSGI_FILE"
    echo "✅ WSGI file touched - app will reload"
else
    echo "⚠️  WSGI file not found at: $WSGI_FILE"
    echo "   You may need to manually reload from Web tab"
fi

# Final summary
echo ""
echo "========================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click the green 'Reload' button"
echo "3. Clear your browser cache (Ctrl+Shift+R)"
echo "4. Visit: https://www.penasia.edu.hk/courses"
echo ""
echo "Expected results:"
echo "  ✓ Hotel Culinary: HK\$125,000"
echo "  ✓ BTEC Business: HK\$118,000"
echo "  ✓ Western Bakery: HK\$12,620"
echo "  ✓ Western Cuisine: HK\$13,200"
echo "  ✓ Each course has unique image"
echo ""
