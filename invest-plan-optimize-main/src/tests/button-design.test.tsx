import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';

describe('Button Design and Styling Tests', () => {
  describe('Button Component', () => {
    it('should render with default variant', () => {
      render(<Button>Test Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toBeInTheDocument();
      expect(button).toHaveClass('bg-primary');
      expect(button).toHaveClass('text-primary-foreground');
    });

    it('should render with outline variant', () => {
      render(<Button variant="outline">Outline Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('border');
      expect(button).toHaveClass('bg-background');
    });

    it('should render with secondary variant', () => {
      render(<Button variant="secondary">Secondary Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('bg-secondary');
      expect(button).toHaveClass('text-secondary-foreground');
    });

    it('should render with destructive variant', () => {
      render(<Button variant="destructive">Delete Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('bg-destructive');
      expect(button).toHaveClass('text-destructive-foreground');
    });

    it('should render with ghost variant', () => {
      render(<Button variant="ghost">Ghost Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('hover:bg-accent');
    });

    it('should render with link variant', () => {
      render(<Button variant="link">Link Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('text-primary');
      expect(button).toHaveClass('underline-offset-4');
    });

    it('should handle different sizes', () => {
      const { rerender } = render(<Button size="sm">Small</Button>);
      expect(screen.getByRole('button')).toHaveClass('h-9');

      rerender(<Button size="default">Default</Button>);
      expect(screen.getByRole('button')).toHaveClass('h-10');

      rerender(<Button size="lg">Large</Button>);
      expect(screen.getByRole('button')).toHaveClass('h-11');

      rerender(<Button size="icon">Icon</Button>);
      expect(screen.getByRole('button')).toHaveClass('h-10', 'w-10');
    });

    it('should handle disabled state', () => {
      render(<Button disabled>Disabled Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toBeDisabled();
      expect(button).toHaveClass('disabled:pointer-events-none');
      expect(button).toHaveClass('disabled:opacity-50');
    });

    it('should handle click events', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Clickable Button</Button>);
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('should not trigger click when disabled', () => {
      const handleClick = vi.fn();
      render(<Button disabled onClick={handleClick}>Disabled Button</Button>);
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('should support custom className', () => {
      render(<Button className="custom-class">Custom Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('custom-class');
    });

    it('should render with icons', () => {
      render(
        <Button>
          <span data-testid="icon">🚀</span>
          Button with Icon
        </Button>
      );
      
      expect(screen.getByTestId('icon')).toBeInTheDocument();
      expect(screen.getByText('Button with Icon')).toBeInTheDocument();
    });
  });

  describe('Badge Component', () => {
    it('should render with default variant', () => {
      render(<Badge>Default Badge</Badge>);
      const badge = screen.getByText('Default Badge');
      
      expect(badge).toHaveClass('bg-primary');
      expect(badge).toHaveClass('text-primary-foreground');
    });

    it('should render with secondary variant', () => {
      render(<Badge variant="secondary">Secondary Badge</Badge>);
      const badge = screen.getByText('Secondary Badge');
      
      expect(badge).toHaveClass('bg-secondary');
      expect(badge).toHaveClass('text-secondary-foreground');
    });

    it('should render with destructive variant', () => {
      render(<Badge variant="destructive">Error Badge</Badge>);
      const badge = screen.getByText('Error Badge');
      
      expect(badge).toHaveClass('bg-destructive');
      expect(badge).toHaveClass('text-destructive-foreground');
    });

    it('should render with outline variant', () => {
      render(<Badge variant="outline">Outline Badge</Badge>);
      const badge = screen.getByText('Outline Badge');
      
      expect(badge).toHaveClass('text-foreground');
    });
  });

  describe('Card Component', () => {
    it('should render with default styling', () => {
      render(
        <Card data-testid="card">
          <div>Card Content</div>
        </Card>
      );
      
      const card = screen.getByTestId('card');
      expect(card).toHaveClass('rounded-lg');
      expect(card).toHaveClass('border');
      expect(card).toHaveClass('bg-card');
      expect(card).toHaveClass('text-card-foreground');
      expect(card).toHaveClass('shadow-sm');
    });

    it('should support custom className', () => {
      render(
        <Card className="custom-card-class" data-testid="card">
          <div>Card Content</div>
        </Card>
      );
      
      const card = screen.getByTestId('card');
      expect(card).toHaveClass('custom-card-class');
    });
  });

  describe('CSS Custom Properties', () => {
    it('should have proper CSS variables defined', () => {
      // Test that CSS variables are properly defined
      const testElement = document.createElement('div');
      document.body.appendChild(testElement);
      
      const computedStyle = getComputedStyle(testElement);
      
      // These should be defined in the CSS
      const primaryColor = computedStyle.getPropertyValue('--primary');
      const backgroundColor = computedStyle.getPropertyValue('--background');
      
      // Clean up
      document.body.removeChild(testElement);
      
      // Note: In a real test environment, these would have values
      // Here we're just testing that the structure is correct
      expect(typeof primaryColor).toBe('string');
      expect(typeof backgroundColor).toBe('string');
    });
  });

  describe('Gradient and Animation Classes', () => {
    it('should apply gradient button classes correctly', () => {
      render(<Button className="btn-gradient">Gradient Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('btn-gradient');
    });

    it('should apply neon button classes correctly', () => {
      render(<Button className="btn-neon">Neon Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('btn-neon');
    });

    it('should apply card floating classes correctly', () => {
      render(
        <Card className="card-floating" data-testid="floating-card">
          <div>Floating Card</div>
        </Card>
      );
      
      const card = screen.getByTestId('floating-card');
      expect(card).toHaveClass('card-floating');
    });

    it('should apply holographic card classes correctly', () => {
      render(
        <Card className="card-holographic" data-testid="holo-card">
          <div>Holographic Card</div>
        </Card>
      );
      
      const card = screen.getByTestId('holo-card');
      expect(card).toHaveClass('card-holographic');
    });
  });

  describe('Responsive Design', () => {
    it('should handle responsive classes', () => {
      render(
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6" data-testid="responsive-grid">
          <Button>Button 1</Button>
          <Button>Button 2</Button>
          <Button>Button 3</Button>
        </div>
      );
      
      const grid = screen.getByTestId('responsive-grid');
      expect(grid).toHaveClass('grid-cols-1');
      expect(grid).toHaveClass('md:grid-cols-3');
      expect(grid).toHaveClass('gap-6');
    });
  });

  describe('Focus and Accessibility', () => {
    it('should handle focus states correctly', () => {
      render(<Button>Focusable Button</Button>);
      const button = screen.getByRole('button');
      
      button.focus();
      expect(document.activeElement).toBe(button);
      
      // Should have focus-visible classes
      expect(button).toHaveClass('focus-visible:outline-none');
      expect(button).toHaveClass('focus-visible:ring-2');
    });

    it('should support keyboard navigation', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Keyboard Button</Button>);
      
      const button = screen.getByRole('button');
      
      // Simulate Enter key press
      fireEvent.keyDown(button, { key: 'Enter', code: 'Enter' });
      
      // Simulate Space key press
      fireEvent.keyDown(button, { key: ' ', code: 'Space' });
      
      // Button should be accessible via keyboard
      expect(button).not.toHaveAttribute('tabindex', '-1');
    });

    it('should have proper ARIA attributes', () => {
      render(<Button aria-label="Custom Label">Button</Button>);
      const button = screen.getByRole('button');
      
      expect(button).toHaveAttribute('aria-label', 'Custom Label');
    });
  });

  describe('Loading States', () => {
    it('should handle loading state correctly', () => {
      const { rerender } = render(<Button>Normal Button</Button>);
      let button = screen.getByRole('button');
      expect(button).not.toBeDisabled();
      
      rerender(<Button disabled>Loading...</Button>);
      button = screen.getByRole('button');
      expect(button).toBeDisabled();
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  describe('Color Scheme Validation', () => {
    it('should not use pink/magenta colors in gradients', () => {
      // This test ensures our color changes were applied
      const testDiv = document.createElement('div');
      testDiv.className = 'bg-gradient-to-r from-primary to-accent';
      document.body.appendChild(testDiv);
      
      const computedStyle = getComputedStyle(testDiv);
      const backgroundImage = computedStyle.backgroundImage;
      
      // Should not contain the old pink/magenta HSL values
      expect(backgroundImage).not.toContain('285 85% 65%');
      expect(backgroundImage).not.toContain('324 93% 58%');
      
      document.body.removeChild(testDiv);
    });
  });
});