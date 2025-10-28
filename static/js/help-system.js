/**
 * PenAsia Help System
 * Provides contextual help, tooltips, and getting started guides
 */

// Help content for different modules
const helpContent = {
    // Admin Dashboard
    admin_dashboard: {
        title: "Admin Dashboard",
        icon: "fa-tachometer-alt",
        sections: [
            {
                heading: "What You Can Do",
                content: "The admin dashboard is your central hub for managing all aspects of the PenAsia system. Monitor key metrics, manage users, and oversee all operations from one place."
            },
            {
                heading: "Key Features",
                items: [
                    "View real-time statistics on applications, students, and courses",
                    "Access quick links to all admin modules",
                    "Monitor pending tasks with badge notifications",
                    "Review recent activity and system status"
                ]
            },
            {
                heading: "Quick Actions",
                items: [
                    "<strong>Applications:</strong> Review and approve/reject student applications",
                    "<strong>Contact Inquiries:</strong> Respond to prospective student inquiries",
                    "<strong>Consultations:</strong> Manage scheduled consultation bookings",
                    "<strong>Courses:</strong> Create and manage course offerings"
                ]
            },
            {
                heading: "Tips",
                content: "Use the badge counters to identify items requiring immediate attention. Click any stat card to navigate directly to that module."
            }
        ]
    },
    
    // Applications Management
    admin_applications: {
        title: "Applications Management",
        icon: "fa-file-alt",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "Review and process all student applications efficiently. Approve qualified candidates, request additional information, or reject applications with feedback."
            },
            {
                heading: "How to Use",
                items: [
                    "<strong>Filter:</strong> Use status tabs (All, Pending, Approved, Rejected) to organize applications",
                    "<strong>Review:</strong> Click on any application to view full details and documents",
                    "<strong>Decide:</strong> Use action buttons to approve or reject applications",
                    "<strong>Communicate:</strong> Add admin notes visible to other staff members"
                ]
            },
            {
                heading: "Application Status Flow",
                content: "<span class='badge bg-warning'>Pending</span> → <span class='badge bg-success'>Approved</span> or <span class='badge bg-danger'>Rejected</span>"
            },
            {
                heading: "Best Practices",
                items: [
                    "Review applications within 48 hours of submission",
                    "Always add notes explaining rejection reasons",
                    "Verify contact information before approving",
                    "Check for duplicate applications from the same email"
                ]
            }
        ]
    },
    
    // Contact Inquiries
    admin_contact: {
        title: "Contact Inquiries",
        icon: "fa-envelope",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "Manage all contact form submissions from prospective students. Track inquiry status and ensure timely responses to maintain excellent customer service."
            },
            {
                heading: "How to Use",
                items: [
                    "<strong>View:</strong> All inquiries display with contact details and message",
                    "<strong>Mark In Progress:</strong> Claim an inquiry when you start working on it",
                    "<strong>Resolve:</strong> Mark as resolved after responding and add resolution notes",
                    "<strong>Reopen:</strong> Reopen resolved inquiries if follow-up is needed"
                ]
            },
            {
                heading: "Status Workflow",
                content: "<span class='badge bg-danger'>New</span> → <span class='badge bg-warning'>In Progress</span> → <span class='badge bg-success'>Resolved</span>"
            },
            {
                heading: "Response Guidelines",
                items: [
                    "Respond to new inquiries within 24 hours",
                    "Personalize responses using the inquirer's name",
                    "Provide clear answers with next steps",
                    "Always document your resolution in admin notes"
                ]
            }
        ]
    },
    
    // Course Management
    admin_courses: {
        title: "Course Management",
        icon: "fa-book",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "Create, edit, and manage all course offerings. Control course visibility, pricing, schedules, and enrollment settings."
            },
            {
                heading: "How to Use",
                items: [
                    "<strong>Create Course:</strong> Click 'Add New Course' and fill in all required details",
                    "<strong>Edit Course:</strong> Click edit icon on any course to modify information",
                    "<strong>Manage Modules:</strong> Add lessons and modules to organize course content",
                    "<strong>Control Visibility:</strong> Toggle published status to show/hide courses"
                ]
            },
            {
                heading: "Course Setup Checklist",
                items: [
                    "✓ Enter course name, code, and description",
                    "✓ Set appropriate duration and credit hours",
                    "✓ Upload course image and set category",
                    "✓ Define pricing (HKD and USD)",
                    "✓ Create modules and lessons",
                    "✓ Set enrollment limits if needed",
                    "✓ Publish when ready"
                ]
            },
            {
                heading: "Tips",
                content: "Keep course descriptions clear and compelling. Include learning outcomes, prerequisites, and career benefits."
            }
        ]
    },
    
    // Student Management
    admin_students: {
        title: "Student Management",
        icon: "fa-user-graduate",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "View and manage all enrolled students. Track their progress, enrollments, and academic records in one centralized location."
            },
            {
                heading: "Key Features",
                items: [
                    "View complete student profiles and contact information",
                    "Track course enrollments and progress",
                    "Monitor assignment submissions and grades",
                    "Access attendance records",
                    "Manage student accounts and permissions"
                ]
            },
            {
                heading: "Common Tasks",
                items: [
                    "<strong>Enroll Student:</strong> Add students to courses manually",
                    "<strong>Update Info:</strong> Edit student contact and profile details",
                    "<strong>View Progress:</strong> Check grades, attendance, and completion status",
                    "<strong>Generate Reports:</strong> Export student data for analysis"
                ]
            }
        ]
    },
    
    // Assignments
    admin_assignments: {
        title: "Assignments Management",
        icon: "fa-tasks",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "Create assignments, review student submissions, and provide grades and feedback efficiently."
            },
            {
                heading: "How to Use",
                items: [
                    "<strong>Create:</strong> Click 'Create Assignment' and set title, description, due date",
                    "<strong>Review:</strong> View all submissions with student details",
                    "<strong>Grade:</strong> Assign scores and write feedback for each submission",
                    "<strong>Track:</strong> Monitor submission rates and pending reviews"
                ]
            },
            {
                heading: "Grading Best Practices",
                items: [
                    "Grade submissions within 5 business days",
                    "Provide constructive, specific feedback",
                    "Use consistent rubrics across students",
                    "Allow resubmissions for low grades when appropriate"
                ]
            }
        ]
    },
    
    // Student Dashboard
    student_dashboard: {
        title: "Student Dashboard",
        icon: "fa-graduation-cap",
        sections: [
            {
                heading: "Your Learning Hub",
                content: "Welcome to your personalized learning portal! Access all your courses, assignments, and academic resources from this central dashboard."
            },
            {
                heading: "What You Can Do",
                items: [
                    "<strong>View Courses:</strong> Access your enrolled courses and learning materials",
                    "<strong>Submit Assignments:</strong> Upload homework and track your grades",
                    "<strong>Check Attendance:</strong> View your attendance record",
                    "<strong>Download Certificates:</strong> Get certificates for completed courses",
                    "<strong>Track Progress:</strong> Monitor your learning progress across all courses"
                ]
            },
            {
                heading: "Getting Started",
                items: [
                    "1. Click on a course to access lessons and materials",
                    "2. Check 'Assignments' for pending homework",
                    "3. Review 'Announcements' for important updates",
                    "4. Use 'Messages' to communicate with instructors"
                ]
            },
            {
                heading: "Tips for Success",
                items: [
                    "Log in regularly to stay updated on course activities",
                    "Submit assignments before due dates",
                    "Participate actively in course discussions",
                    "Contact instructors if you need help"
                ]
            }
        ]
    },
    
    // Consultations
    admin_consultations: {
        title: "Consultations Management",
        icon: "fa-calendar-check",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "Manage all consultation bookings from prospective students. Schedule appointments, track attendance, and follow up effectively."
            },
            {
                heading: "How to Use",
                items: [
                    "<strong>View Bookings:</strong> See all scheduled consultations with details",
                    "<strong>Confirm:</strong> Approve consultation requests",
                    "<strong>Complete:</strong> Mark consultations as completed after meeting",
                    "<strong>Cancel:</strong> Cancel and reschedule if needed"
                ]
            },
            {
                heading: "Status Workflow",
                content: "<span class='badge bg-warning'>Pending</span> → <span class='badge bg-info'>Confirmed</span> → <span class='badge bg-success'>Completed</span>"
            },
            {
                heading: "Best Practices",
                items: [
                    "Confirm bookings within 24 hours",
                    "Send reminder emails 1 day before consultation",
                    "Prepare talking points based on program interest",
                    "Follow up within 3 days after consultation"
                ]
            }
        ]
    },
    
    // Attendance
    admin_attendance: {
        title: "Attendance Management",
        icon: "fa-clipboard-check",
        sections: [
            {
                heading: "What You Can Achieve",
                content: "Record and track student attendance for all courses. Generate reports and identify students with attendance issues."
            },
            {
                heading: "How to Use",
                items: [
                    "<strong>Select Course:</strong> Choose the course and date",
                    "<strong>Mark Attendance:</strong> Check present/absent for each student",
                    "<strong>Add Notes:</strong> Record reasons for absences",
                    "<strong>Submit:</strong> Save attendance record"
                ]
            },
            {
                heading: "Attendance Policies",
                items: [
                    "Students must maintain 80% attendance",
                    "3 consecutive absences trigger automatic alert",
                    "Late arrivals (>15 mins) marked as partial attendance",
                    "Medical certificates required for sick leave"
                ]
            }
        ]
    }
};

/**
 * Initialize help system
 */
function initHelpSystem() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add help button click handlers
    document.querySelectorAll('.help-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const module = this.getAttribute('data-module');
            showHelpModal(module);
        });
    });
    
    // Check if user is new and show getting started guide
    if (shouldShowGettingStarted()) {
        setTimeout(() => showGettingStartedGuide(), 1000);
    }
}

/**
 * Show help modal for specific module
 */
function showHelpModal(moduleName) {
    const content = helpContent[moduleName];
    if (!content) return;
    
    let modalHTML = `
        <div class="modal fade" id="helpModal" tabindex="-1" aria-labelledby="helpModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title" id="helpModalLabel">
                            <i class="fas ${content.icon} me-2"></i>${content.title} - Help Guide
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
    `;
    
    content.sections.forEach(section => {
        modalHTML += `<div class="mb-4">`;
        if (section.heading) {
            modalHTML += `<h6 class="text-primary fw-bold mb-3"><i class="fas fa-info-circle me-2"></i>${section.heading}</h6>`;
        }
        if (section.content) {
            modalHTML += `<p>${section.content}</p>`;
        }
        if (section.items) {
            modalHTML += `<ul class="list-unstyled ms-3">`;
            section.items.forEach(item => {
                modalHTML += `<li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>${item}</li>`;
            });
            modalHTML += `</ul>`;
        }
        modalHTML += `</div>`;
    });
    
    modalHTML += `
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="fas fa-times me-1"></i>Close
                        </button>
                        <button type="button" class="btn btn-primary" onclick="window.open('mailto:support@penasia.edu.hk?subject=Help Request: ${content.title}')">
                            <i class="fas fa-question-circle me-1"></i>Need More Help?
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if present
    const existingModal = document.getElementById('helpModal');
    if (existingModal) existingModal.remove();
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('helpModal'));
    modal.show();
    
    // Cleanup on close
    document.getElementById('helpModal').addEventListener('hidden.bs.modal', function () {
        this.remove();
    });
}

/**
 * Check if getting started guide should be shown
 */
function shouldShowGettingStarted() {
    // Check if user has seen the guide (stored in localStorage)
    const hasSeenGuide = localStorage.getItem('penasia_seen_getting_started');
    const userRole = document.body.getAttribute('data-user-role');
    
    // Show for new users only
    return !hasSeenGuide && (userRole === 'student' || userRole === 'admin');
}

/**
 * Show getting started guide
 */
function showGettingStartedGuide() {
    const userRole = document.body.getAttribute('data-user-role');
    const isAdmin = userRole === 'admin';
    
    const guideHTML = `
        <div class="modal fade" id="gettingStartedModal" tabindex="-1" aria-labelledby="gettingStartedLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-gradient" style="background: linear-gradient(135deg, #1B365D 0%, #2E5984 100%);">
                        <h5 class="modal-title text-white" id="gettingStartedLabel">
                            <i class="fas fa-rocket me-2"></i>Welcome to PenAsia!
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <i class="fas fa-${isAdmin ? 'user-shield' : 'graduation-cap'} text-primary" style="font-size: 3rem;"></i>
                            <h4 class="mt-3 text-primary">Let's Get You Started!</h4>
                            <p class="text-muted">Here's a quick guide to help you navigate the platform</p>
                        </div>
                        
                        ${isAdmin ? `
                        <div class="row g-3">
                            <div class="col-md-6">
                                <div class="card h-100 border-primary">
                                    <div class="card-body">
                                        <h6 class="text-primary"><i class="fas fa-tachometer-alt me-2"></i>Dashboard Overview</h6>
                                        <p class="small mb-0">Monitor key metrics and access all admin functions from your dashboard.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-success">
                                    <div class="card-body">
                                        <h6 class="text-success"><i class="fas fa-file-alt me-2"></i>Review Applications</h6>
                                        <p class="small mb-0">Check for new student applications requiring your review.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-warning">
                                    <div class="card-body">
                                        <h6 class="text-warning"><i class="fas fa-envelope me-2"></i>Contact Inquiries</h6>
                                        <p class="small mb-0">Respond to prospective student inquiries promptly.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-info">
                                    <div class="card-body">
                                        <h6 class="text-info"><i class="fas fa-book me-2"></i>Manage Courses</h6>
                                        <p class="small mb-0">Create and organize course offerings and content.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="alert alert-info mt-4 mb-0">
                            <i class="fas fa-lightbulb me-2"></i><strong>Pro Tip:</strong> Look for the 
                            <i class="fas fa-question-circle text-primary mx-1"></i> help icon in each module for detailed guidance!
                        </div>
                        ` : `
                        <div class="row g-3">
                            <div class="col-md-6">
                                <div class="card h-100 border-primary">
                                    <div class="card-body">
                                        <h6 class="text-primary"><i class="fas fa-book-reader me-2"></i>Access Your Courses</h6>
                                        <p class="small mb-0">Click on any enrolled course to view lessons and materials.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-success">
                                    <div class="card-body">
                                        <h6 class="text-success"><i class="fas fa-tasks me-2"></i>Submit Assignments</h6>
                                        <p class="small mb-0">Upload your homework before the due date to get graded.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-warning">
                                    <div class="card-body">
                                        <h6 class="text-warning"><i class="fas fa-calendar-check me-2"></i>Check Attendance</h6>
                                        <p class="small mb-0">Monitor your attendance record and maintain good standing.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-info">
                                    <div class="card-body">
                                        <h6 class="text-info"><i class="fas fa-certificate me-2"></i>Get Certificates</h6>
                                        <p class="small mb-0">Download certificates when you complete courses.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="alert alert-info mt-4 mb-0">
                            <i class="fas fa-lightbulb me-2"></i><strong>Pro Tip:</strong> Hover over features to see quick tooltips, and click the 
                            <i class="fas fa-question-circle text-primary mx-1"></i> help icon for detailed guides!
                        </div>
                        `}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" onclick="remindMeLater()">
                            <i class="fas fa-clock me-1"></i>Remind Me Later
                        </button>
                        <button type="button" class="btn btn-primary" onclick="dismissGettingStarted()">
                            <i class="fas fa-check me-1"></i>Got It, Thanks!
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', guideHTML);
    const modal = new bootstrap.Modal(document.getElementById('gettingStartedModal'));
    modal.show();
    
    // Cleanup on close
    document.getElementById('gettingStartedModal').addEventListener('hidden.bs.modal', function () {
        this.remove();
    });
}

/**
 * Dismiss getting started guide permanently
 */
function dismissGettingStarted() {
    localStorage.setItem('penasia_seen_getting_started', 'true');
    const modal = bootstrap.Modal.getInstance(document.getElementById('gettingStartedModal'));
    modal.hide();
}

/**
 * Remind user later (next session)
 */
function remindMeLater() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('gettingStartedModal'));
    modal.hide();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initHelpSystem);
