package com.devops;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main Application Class
 * DevOps Java Application using Gradle
 */
public class App {
    private static final Logger logger = LoggerFactory.getLogger(App.class);
    
    public static void main(String[] args) {
        logger.info("Starting DevOps Java Application");
        
        Calculator calculator = new Calculator();
        
        System.out.println("=== DevOps Java Application ===");
        System.out.println("Built with Gradle");
        System.out.println();
        
        int a = 15;
        int b = 5;
        
        System.out.println("Performing calculations:");
        System.out.println(a + " + " + b + " = " + calculator.add(a, b));
        System.out.println(a + " - " + b + " = " + calculator.subtract(a, b));
        System.out.println(a + " * " + b + " = " + calculator.multiply(a, b));
        System.out.println(a + " / " + b + " = " + calculator.divide(a, b));
        
        logger.info("Application completed successfully");
    }
}

