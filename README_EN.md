# Comprehensive Life Management App

A comprehensive productivity and life management application built with Flask. Manage your tasks, habits, health, learning, and more - all in one place with complete privacy (100% local storage).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.0-green.svg)

## 🌟 Features

### Productivity
- **⏱️ Focus Timer**: 25-minute focus sessions with 5-minute breaks (Pomodoro Technique)
- **✅ To-Do List**: Task management with priorities and deadlines
- **🎯 Goal Setting**: Short-term, mid-term, and long-term goal tracking
- **⏰ Time Tracking**: Project-based time tracking

### Life Management
- **🔄 Habit Tracker**: Daily habit tracking with streak counting
- **💪 Health Management**: Weight, exercise, and sleep tracking
- **📚 Learning Management**: Track learning progress and study hours
- **📔 Journal**: Daily reflection and journaling
- **📝 Quick Notes**: Fast note-taking

### Analytics & Insights
- **📊 Visual Analytics**: View your activities in graphs and charts
- **📈 Weekly/Monthly Reports**: Comprehensive activity summaries
- **🏆 Achievement Badges**: Earn badges for your accomplishments
- **📅 Calendar**: Integrated calendar view with all your activities

## 🔒 Privacy First

- **100% Local Storage**: All data is stored on your PC only
- **No External Transmission**: No data sent to external servers
- **No Third-Party Sharing**: Your data stays with you
- **No Tracking**: No analytics or tracking cookies
- **Offline Capable**: Works without internet connection

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
```bash
git clone https://github.com/yourusername/remote-productivity.git
cd remote-productivity
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://localhost:5001
```

## 📦 Dependencies

- Flask 2.3.0 - Web framework
- Flask-SQLAlchemy 3.0.3 - Database ORM
- Flask-WTF 1.1.1 - CSRF protection
- Werkzeug 2.3.7 - WSGI utilities
- python-dotenv 1.0.0 - Environment variables

## 📖 User Guide

### First Time Setup

1. **Accept Terms**: On first launch, you'll be asked to accept the Terms of Service and Privacy Policy
2. **Start Using**: After accepting, you can start using all features immediately
3. **Backup Regularly**: Set up weekly backups from the Settings page

### Core Features

#### Focus Timer
1. Navigate to "Focus Timer" from the menu
2. Select a task (optional)
3. Click "Start" to begin a 25-minute focus session
4. Take a 5-minute break when the timer completes
5. Repeat for maximum productivity

#### To-Do List
1. Click "To-Do List" in the menu
2. Click "Add Task" button
3. Enter task details (title, priority, deadline)
4. Track your progress
5. Mark as complete when done

#### Habit Tracker
1. Go to "Habits" page
2. Add daily habits you want to track
3. Check off habits as you complete them
4. Build streaks and stay motivated

#### Calendar
1. Click on any date to add an event
2. Set reminders (30 minutes before)
3. View all your activities in one place
4. Color-coded by category

### Data Management

#### Backup Your Data
1. Go to Settings → Data Management
2. Click "Download Backup" for database backup
3. Click "Download JSON" for human-readable export
4. Store backups in a safe location

#### Restore Data
1. Close the application
2. Rename your backup file to `productivity.db`
3. Place it in the application folder
4. Restart the application

## 🛡️ Security

### Implemented Security Measures

- ✅ **CSRF Protection**: Prevents cross-site request forgery attacks
- ✅ **XSS Prevention**: All user inputs are sanitized
- ✅ **SQL Injection Protection**: Using SQLAlchemy ORM
- ✅ **Input Validation**: All inputs are validated and sanitized
- ✅ **Security Headers**: Comprehensive security headers implemented

See [SECURITY.md](SECURITY.md) for detailed security information.

## 📁 Project Structure

```
remote-productivity/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── productivity.db        # SQLite database (created on first run)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── dashboard.html    # Dashboard page
│   ├── pomodoro.html     # Focus timer page
│   ├── tasks.html        # To-do list page
│   ├── habits.html       # Habit tracker page
│   ├── calendar.html     # Calendar page
│   └── ...               # Other templates
├── static/               # Static files (if any)
├── SECURITY.md           # Security policy
├── TERMINOLOGY.md        # Terminology guide
└── README.md             # This file
```

## 🎯 Use Cases

### For Remote Workers
- Track work hours with time tracking
- Manage tasks and deadlines
- Stay focused with the focus timer
- Review productivity with analytics

### For Students
- Track study sessions
- Manage assignments and deadlines
- Monitor learning progress
- Build study habits

### For Personal Development
- Track daily habits
- Monitor health metrics
- Set and achieve goals
- Reflect with journaling

### For Anyone
- Organize daily tasks
- Build positive habits
- Track personal goals
- Maintain work-life balance

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-random-secret-key-here
```

### Settings

Customize the focus timer durations:
1. Go to Settings page
2. Adjust work duration (5-60 minutes)
3. Adjust break duration (1-30 minutes)
4. Adjust long break duration (5-60 minutes)

## 📊 Achievement Badges

Earn badges by using the app:

- **🎯 First Step**: Complete 1 focus session
- **⏱️ Timer Beginner**: Complete 10 focus sessions
- **🏆 Timer Master**: Complete 100 focus sessions
- **🔥 Habit Power**: 7-day habit streak
- **💪 Persistence**: 30-day habit streak
- **✅ Task Hunter**: Complete 50 tasks

## 🌐 Supported Languages

- Japanese (日本語) - Primary
- English - This README

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

- **Email**: your-email@example.com
- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/remote-productivity/issues)

## ❓ FAQ

### Is my data safe?
Yes! All data is stored locally on your PC. Nothing is sent to external servers.

### Can I use this on multiple computers?
Yes! Use the backup/restore feature to transfer your data between computers.

### Does this require internet?
No! The app works completely offline. Internet is only needed for initial installation.

### How do I backup my data?
Go to Settings → Data Management → Download Backup. Save the file in a safe location.

### What if I lose my data?
Restore from your backup file. This is why regular backups are important!

### Can I customize the focus timer duration?
Yes! Go to Settings and adjust the durations to your preference.

### Is there a mobile app?
Not currently. This is a web-based application that runs locally on your computer.

### Can multiple users use this?
This app is designed for single-user use. Each user should have their own installation.

## 🗺️ Roadmap

### Planned Features
- [ ] Data encryption
- [ ] User authentication (multi-user support)
- [ ] Mobile responsive design improvements
- [ ] Dark mode
- [ ] Export to PDF reports
- [ ] Integration with external calendars
- [ ] Customizable themes

### Future Enhancements
- [ ] API for third-party integrations
- [ ] Plugin system
- [ ] Cloud sync (optional)
- [ ] Mobile app

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- UI powered by [Bootstrap 5](https://getbootstrap.com/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)
- Inspired by productivity methodologies and personal development practices

## 📚 Documentation

- [Security Policy](SECURITY.md) - Security measures and best practices
- [Terminology Guide](TERMINOLOGY.md) - User-friendly terminology (Japanese)
- [Terms of Service](http://localhost:5001/terms) - Usage terms
- [Privacy Policy](http://localhost:5001/privacy) - Privacy information

## 🎓 Learning Resources

### Productivity Techniques
- **Pomodoro Technique**: 25-minute focus sessions
- **GTD (Getting Things Done)**: Task management methodology
- **Habit Stacking**: Building new habits

### Time Management
- **Time Blocking**: Schedule specific time slots
- **Priority Matrix**: Urgent vs Important
- **Weekly Reviews**: Reflect and plan

## 💡 Tips for Success

1. **Start Small**: Don't try to track everything at once
2. **Be Consistent**: Use the app daily for best results
3. **Review Regularly**: Check your analytics weekly
4. **Backup Often**: Set a weekly backup reminder
5. **Customize**: Adjust settings to match your workflow
6. **Celebrate Wins**: Acknowledge your achievements

## 🐛 Known Issues

- None currently reported

## 📈 Version History

### v1.0.0 (2025-10-07)
- Initial release
- Core productivity features
- Life management tools
- Analytics and reporting
- Achievement system
- Security enhancements
- Privacy-first design

---

**Made with ❤️ for productivity enthusiasts**

**Remember**: This app is a tool to help you, not control you. Use it in a way that works best for your lifestyle and goals.
