from app import db, app
from models.chapter import Chapter, ChapterObjective

def seed_chapters():
    # Clear existing data
    ChapterObjective.query.delete()
    Chapter.query.delete()
    
    # Define chapter content for each language and level
    roadmap_data = {
        'python': {
            'beginner': [
                {
                    'number': 1,
                    'title': 'Introduction to Python',
                    'description': 'Get started with Python programming language fundamentals',
                    'objectives': [
                        'Understand what Python is and its applications',
                        'Set up Python development environment',
                        'Learn basic syntax and data types',
                        'Write your first Python program'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Control Flow',
                    'description': 'Learn how to control program flow using conditions and loops',
                    'objectives': [
                        'Master if-else statements and conditional logic',
                        'Implement while and for loops effectively',
                        'Understand break and continue statements',
                        'Practice with basic control flow exercises'
                    ]
                },
                {
                    'number': 3,
                    'title': 'Functions and Modules',
                    'description': 'Learn to write reusable code using functions and modules',
                    'objectives': [
                        'Define and call functions',
                        'Understand function parameters and return values',
                        'Work with built-in modules',
                        'Create custom modules'
                    ]
                }
            ],
            'intermediate': [
                {
                    'number': 1,
                    'title': 'Object-Oriented Programming',
                    'description': 'Master object-oriented programming concepts in Python',
                    'objectives': [
                        'Understand classes and objects',
                        'Implement inheritance and polymorphism',
                        'Work with class methods and properties',
                        'Practice encapsulation and abstraction'
                    ]
                },
                {
                    'number': 2,
                    'title': 'File Handling and Exception Management',
                    'description': 'Learn to work with files and handle errors gracefully',
                    'objectives': [
                        'Read and write files in Python',
                        'Handle different file formats (txt, csv, json)',
                        'Implement try-except blocks',
                        'Create custom exceptions'
                    ]
                }
            ],
            'advanced': [
                {
                    'number': 1,
                    'title': 'Advanced Python Concepts',
                    'description': 'Explore advanced Python features and patterns',
                    'objectives': [
                        'Master decorators and generators',
                        'Understand context managers',
                        'Work with metaclasses',
                        'Implement design patterns in Python'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Concurrent Programming',
                    'description': 'Learn parallel and asynchronous programming',
                    'objectives': [
                        'Understand threading and multiprocessing',
                        'Master asyncio for async programming',
                        'Handle race conditions and deadlocks',
                        'Build concurrent applications'
                    ]
                }
            ]
        },
        'cpp': {
            'beginner': [
                {
                    'number': 1,
                    'title': 'Introduction to C++',
                    'description': 'Get started with C++ programming fundamentals',
                    'objectives': [
                        'Understand C++ basics and syntax',
                        'Set up C++ development environment',
                        'Learn variables and data types',
                        'Write basic C++ programs'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Control Structures',
                    'description': 'Master program flow control in C++',
                    'objectives': [
                        'Implement if-else statements',
                        'Work with loops (for, while)',
                        'Use switch statements',
                        'Practice with control structures'
                    ]
                }
            ],
            'intermediate': [
                {
                    'number': 1,
                    'title': 'Object-Oriented C++',
                    'description': 'Learn object-oriented programming in C++',
                    'objectives': [
                        'Create classes and objects',
                        'Implement inheritance',
                        'Use virtual functions',
                        'Work with operator overloading'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Memory Management',
                    'description': 'Understanding C++ memory management',
                    'objectives': [
                        'Work with pointers and references',
                        'Manage dynamic memory allocation',
                        'Prevent memory leaks',
                        'Implement smart pointers'
                    ]
                }
            ],
            'advanced': [
                {
                    'number': 1,
                    'title': 'Templates and STL',
                    'description': 'Master C++ templates and Standard Template Library',
                    'objectives': [
                        'Create function and class templates',
                        'Use STL containers and algorithms',
                        'Implement template metaprogramming',
                        'Work with iterators and functors'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Modern C++ Features',
                    'description': 'Explore modern C++ features and best practices',
                    'objectives': [
                        'Use lambda expressions',
                        'Implement move semantics',
                        'Work with C++17/20 features',
                        'Master RAII and smart pointers'
                    ]
                }
            ]
        },
        'java': {
            'beginner': [
                {
                    'number': 1,
                    'title': 'Java Fundamentals',
                    'description': 'Learn the basics of Java programming',
                    'objectives': [
                        'Set up Java development environment',
                        'Understand Java syntax and structure',
                        'Work with variables and data types',
                        'Write basic Java programs'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Control Flow and Arrays',
                    'description': 'Master control structures and arrays in Java',
                    'objectives': [
                        'Implement conditional statements',
                        'Work with loops and arrays',
                        'Handle basic input/output',
                        'Practice with coding exercises'
                    ]
                }
            ],
            'intermediate': [
                {
                    'number': 1,
                    'title': 'Object-Oriented Java',
                    'description': 'Master object-oriented programming in Java',
                    'objectives': [
                        'Create classes and objects',
                        'Implement inheritance and interfaces',
                        'Use abstract classes',
                        'Work with packages'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Exception Handling and Collections',
                    'description': 'Learn to handle errors and work with collections',
                    'objectives': [
                        'Implement try-catch blocks',
                        'Work with checked exceptions',
                        'Use ArrayList and LinkedList',
                        'Master Java Collections Framework'
                    ]
                }
            ],
            'advanced': [
                {
                    'number': 1,
                    'title': 'Multithreading and Concurrency',
                    'description': 'Learn concurrent programming in Java',
                    'objectives': [
                        'Create and manage threads',
                        'Implement synchronization',
                        'Use ExecutorService',
                        'Handle concurrent collections'
                    ]
                },
                {
                    'number': 2,
                    'title': 'Advanced Java Features',
                    'description': 'Explore advanced Java concepts and patterns',
                    'objectives': [
                        'Work with Generics',
                        'Implement design patterns',
                        'Use Java Stream API',
                        'Master Lambda expressions'
                    ]
                }
            ]
        }
    }

    # Add chapters and objectives to database
    for language, levels in roadmap_data.items():
        for level, chapters in levels.items():
            for chapter_data in chapters:
                chapter = Chapter(
                    language=language,
                    level=level,
                    chapter_number=chapter_data['number'],
                    title=chapter_data['title'],
                    description=chapter_data['description']
                )
                db.session.add(chapter)
                db.session.flush()  # To get the chapter ID

                # Add objectives for this chapter
                for i, objective_text in enumerate(chapter_data['objectives'], 1):
                    objective = ChapterObjective(
                        chapter_id=chapter.id,
                        objective_text=objective_text,
                        order=i
                    )
                    db.session.add(objective)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_chapters()
        print("Database seeded successfully!") 