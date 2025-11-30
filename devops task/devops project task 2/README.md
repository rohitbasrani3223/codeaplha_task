# DevOps Java Application using Gradle

This project demonstrates a complete Java application built with Gradle, including CI/CD pipeline integration for continuous delivery.

## Project Overview

This is a simple Java application that performs basic arithmetic operations, built using Gradle build automation tool. The project includes:

- **Gradle Build System**: Automated build and dependency management
- **Java Application**: Calculator application with logging
- **Unit Tests**: JUnit test cases for validation
- **CI/CD Pipeline**: Jenkins pipeline for continuous integration and delivery

## Prerequisites

- Java JDK 11 or higher
- Gradle 7.6 or higher (or use Gradle Wrapper)
- Jenkins (for CI/CD pipeline)

## Project Structure

```
.
├── build.gradle              # Gradle build configuration
├── gradlew                   # Gradle wrapper script (Unix)
├── gradlew.bat              # Gradle wrapper script (Windows)
├── Jenkinsfile              # CI/CD pipeline configuration
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── devops/
│   │               ├── App.java          # Main application class
│   │               └── Calculator.java   # Calculator utility class
│   └── test/
│       └── java/
│           └── com/
│               └── devops/
│                   └── CalculatorTest.java  # Unit tests
└── README.md
```

## Features

### 1. Automated Java Project Builds using Gradle
- Gradle manages the entire build lifecycle
- Automatic dependency resolution from Maven Central
- Compilation, testing, and packaging automation

### 2. Efficient Dependency Management
- Dependencies defined in `build.gradle`
- Automatic version management
- Transitive dependency resolution

### 3. CI/CD Pipeline Integration
- Jenkins pipeline for continuous delivery
- Automated build, test, and package stages
- Artifact archiving for deployment

### 4. Streamlined Build and Deployment Processes
- Single command build: `./gradlew build`
- Automated testing before packaging
- Ready-to-deploy JAR artifacts

### 5. Core DevOps Principles
- Version control integration
- Automated testing
- Continuous integration
- Build automation
- Artifact management

## Building the Project

### Using Gradle Wrapper (Recommended)

**Windows:**
```bash
gradlew.bat build
```

**Linux/Mac:**
```bash
./gradlew build
```

### Using Gradle directly
```bash
gradle build
```

## Running the Application

### Using Gradle Application Plugin
```bash
./gradlew run
```

### Using JAR file
```bash
./gradlew jar
java -jar build/libs/devops-java-app-1.0.0.jar
```

## Running Tests

```bash
./gradlew test
```

Test reports will be generated in `build/reports/tests/test/`

## CI/CD Pipeline

The project includes a Jenkinsfile that defines a complete CI/CD pipeline with the following stages:

1. **Checkout**: Retrieves source code from repository
2. **Build**: Compiles the Java application
3. **Test**: Runs unit tests and generates reports
4. **Package**: Creates JAR artifact
5. **Deploy**: Ready for deployment (customize as needed)

### Setting up Jenkins Pipeline

1. Create a new Jenkins Pipeline job
2. Point it to your repository containing this Jenkinsfile
3. Jenkins will automatically detect and run the pipeline

## Dependencies

- **JUnit 4.13.2**: Testing framework
- **SLF4J 1.7.36**: Logging API
- **Logback 1.2.12**: Logging implementation

## Build Artifacts

After building, the following artifacts are generated:

- `build/libs/devops-java-app-1.0.0.jar`: Executable JAR file
- `build/reports/tests/test/`: HTML test reports
- `build/test-results/`: XML test results

## Development

### Adding New Dependencies

Edit `build.gradle` and add dependencies in the `dependencies` block:

```gradle
dependencies {
    implementation 'group:artifact:version'
}
```

### Running Specific Tasks

```bash
./gradlew tasks          # List all available tasks
./gradlew clean          # Clean build directory
./gradlew compileJava    # Compile only Java sources
./gradlew test           # Run tests only
```

## DevOps Best Practices Implemented

✅ **Infrastructure as Code**: Build configuration in version control  
✅ **Automated Testing**: Unit tests run automatically  
✅ **Continuous Integration**: Jenkins pipeline for automated builds  
✅ **Artifact Management**: Versioned JAR files for deployment  
✅ **Dependency Management**: Centralized and automated  
✅ **Build Reproducibility**: Gradle wrapper ensures consistent builds  

## License

This project is created for educational purposes as part of DevOps training.

## Author

DevOps Project Task 3 - Java Application using Gradle

