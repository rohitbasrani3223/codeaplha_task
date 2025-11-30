package com.devops;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Unit tests for Calculator class
 */
public class CalculatorTest {
    
    private Calculator calculator = new Calculator();
    
    @Test
    public void testAdd() {
        assertEquals(10, calculator.add(5, 5));
        assertEquals(0, calculator.add(-5, 5));
    }
    
    @Test
    public void testSubtract() {
        assertEquals(5, calculator.subtract(10, 5));
        assertEquals(-10, calculator.subtract(-5, 5));
    }
    
    @Test
    public void testMultiply() {
        assertEquals(25, calculator.multiply(5, 5));
        assertEquals(0, calculator.multiply(0, 5));
    }
    
    @Test
    public void testDivide() {
        assertEquals(2, calculator.divide(10, 5));
        assertEquals(5, calculator.divide(25, 5));
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testDivideByZero() {
        calculator.divide(10, 0);
    }
}

