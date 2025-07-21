/**
 * Test setup configuration for Vitest
 * 
 * Configures the testing environment with necessary polyfills
 * and global setup for DOM testing.
 */

import { vi } from 'vitest';

// Mock fetch globally for all tests
global.fetch = vi.fn();

// Mock Bootstrap components
global.bootstrap = {
    Modal: vi.fn().mockImplementation(() => ({
        show: vi.fn(),
        hide: vi.fn()
    })),
    Toast: vi.fn().mockImplementation(() => ({
        show: vi.fn(),
        hide: vi.fn()
    }))
};

// Setup DOM environment
Object.defineProperty(window, 'location', {
    value: {
        href: 'http://localhost:3000',
        origin: 'http://localhost:3000'
    },
    writable: true
});

// Mock console methods for cleaner test output
global.console = {
    ...console,
    error: vi.fn(),
    warn: vi.fn(),
    log: vi.fn()
};

// Reset mocks before each test
beforeEach(() => {
    vi.clearAllMocks();
    fetch.mockClear();
});
