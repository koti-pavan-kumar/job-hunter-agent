#!/bin/bash

# Job Hunter Agent - Autonomous Mode Launcher
# Linux/Mac Bash Script

echo "============================================================"
echo "           JOB HUNTER AGENT - AUTONOMOUS MODE"
echo "============================================================"
echo ""
echo "Starting fully autonomous job hunter..."
echo ""
echo "This agent will:"
echo "  - Search jobs at 8:00 AM and 6:00 PM daily"
echo "  - Check company legitimacy automatically"
echo "  - Generate tailored resumes for matching jobs"
echo "  - Generate cover letters"
echo "  - Save everything in 'job_hunter/resumes/' folder"
echo ""
echo "You just need to:"
echo "  1. Check the 'job_hunter/resumes/' folder"
echo "  2. Review the generated resumes"
echo "  3. Apply to the ones you like when you have time"
echo ""
echo "Press Ctrl+C to stop."
echo "============================================================"
echo ""

python3 -m job_hunter run --immediate
