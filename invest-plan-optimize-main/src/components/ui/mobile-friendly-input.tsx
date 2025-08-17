import * as React from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Input } from "./input";
import { Button } from "./button";
import { useMobileDetection } from "@/hooks/useMobileDetection";

interface MobileFriendlyInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onClear?: () => void;
  showClearButton?: boolean;
  label?: string;
}

export const MobileFriendlyInput = React.forwardRef<HTMLInputElement, MobileFriendlyInputProps>(
  ({ className, onClear, showClearButton = true, label, value, onChange, ...props }, ref) => {
    const { isMobile, isTouchDevice } = useMobileDetection();
    const [displayValue, setDisplayValue] = React.useState('');
    
    // Convert numeric value to string for display, handling empty/zero cases properly
    React.useEffect(() => {
      if (value === undefined || value === null || value === '') {
        setDisplayValue('');
      } else if (typeof value === 'number') {
        // For number inputs, show empty string for zero to avoid leading zeros
        if (props.type === 'number' && value === 0) {
          setDisplayValue('');
        } else {
          setDisplayValue(value.toString());
        }
      } else {
        // Clean up string values to remove leading zeros
        const cleanValue = value.toString().replace(/^0+(?=\d)/, '');
        setDisplayValue(cleanValue);
      }
    }, [value, props.type]);

    const hasValue = displayValue !== '';

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      let inputValue = e.target.value;
      
      // For number inputs, clean up leading zeros
      if (props.type === 'number' && inputValue !== '') {
        // Remove leading zeros but keep single zero or decimal values
        if (inputValue !== '0' && !inputValue.startsWith('0.')) {
          inputValue = inputValue.replace(/^0+/, '') || '0';
          if (inputValue === '') inputValue = '0';
        }
      }
      
      setDisplayValue(inputValue);
      
      if (onChange) {
        // For number inputs, we need to handle the conversion properly
        if (props.type === 'number') {
          // Allow empty string to clear the field
          if (inputValue === '' || inputValue === '0') {
            const syntheticEvent = {
              ...e,
              target: { ...e.target, value: inputValue === '0' ? '0' : '' }
            };
            onChange(syntheticEvent);
          } else {
            // Only parse if there's a valid number
            const numValue = parseFloat(inputValue);
            if (!isNaN(numValue)) {
              const syntheticEvent = {
                ...e,
                target: { ...e.target, value: inputValue }
              };
              onChange(syntheticEvent);
            }
          }
        } else {
          onChange(e);
        }
      }
    };

    const handleClear = () => {
      setDisplayValue('');
      if (onClear) {
        onClear();
      } else if (onChange) {
        // Create a synthetic event to clear the input
        const syntheticEvent = {
          target: { value: '' },
          currentTarget: { value: '' }
        } as React.ChangeEvent<HTMLInputElement>;
        onChange(syntheticEvent);
      }
    };

    return (
      <div className="relative">
        {label && (
          <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 mb-2 block">
            {label}
          </label>
        )}
        
        <div className="relative">
          <Input
            ref={ref}
            className={cn(
              className,
              // Add padding for clear button on mobile
              isMobile && showClearButton && hasValue && "pr-10"
            )}
            value={displayValue}
            onChange={handleInputChange}
            {...props}
          />
          
          {/* Clear button - more prominent on mobile/touch devices */}
          {(isMobile || isTouchDevice) && showClearButton && hasValue && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 p-0 hover:bg-destructive/10 hover:text-destructive mobile-touch-target"
              onClick={handleClear}
              tabIndex={-1}
            >
              <X className="h-4 w-4" />
              <span className="sr-only">Limpar campo</span>
            </Button>
          )}
          
          {/* Desktop clear button - smaller and less intrusive */}
          {!isMobile && !isTouchDevice && showClearButton && hasValue && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6 p-0 opacity-50 hover:opacity-100 hover:bg-destructive/10 hover:text-destructive"
              onClick={handleClear}
              tabIndex={-1}
            >
              <X className="h-3 w-3" />
              <span className="sr-only">Limpar campo</span>
            </Button>
          )}
        </div>
        
        {/* Mobile helper text */}
        {(isMobile || isTouchDevice) && props.type === 'number' && (
          <p className="text-xs text-muted-foreground mt-1">
            Toque no ✕ para zerar o valor
          </p>
        )}
      </div>
    );
  }
);

MobileFriendlyInput.displayName = "MobileFriendlyInput";