import * as React from "react";
import { ChevronDown, Check } from "lucide-react";
import { cn } from "@/lib/utils";
import { useMobileDetection } from "@/hooks/useMobileDetection";

interface CustomSelectProps {
  value: string;
  onValueChange: (value: string) => void;
  options: { value: string; label: string }[];
  placeholder?: string;
  className?: string;
  id?: string;
}

export const CustomSelect = React.forwardRef<HTMLDivElement, CustomSelectProps>(
  ({ value, onValueChange, options, placeholder = "Selecione...", className, id }, ref) => {
    const [isOpen, setIsOpen] = React.useState(false);
    const [selectedValue, setSelectedValue] = React.useState(value);
    const dropdownRef = React.useRef<HTMLDivElement>(null);
    const { isMobile, isTouchDevice } = useMobileDetection();

    React.useEffect(() => {
      setSelectedValue(value);
    }, [value]);

    React.useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
          setIsOpen(false);
        }
      };

      if (isOpen) {
        document.addEventListener('mousedown', handleClickOutside);
        // Prevent body scroll on mobile when dropdown is open
        if (isMobile || isTouchDevice) {
          document.body.style.overflow = 'hidden';
        }
      }

      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        if (isMobile || isTouchDevice) {
          document.body.style.overflow = 'unset';
        }
      };
    }, [isOpen, isMobile, isTouchDevice]);

    const handleSelect = (optionValue: string) => {
      console.log('CustomSelect: Selecionando', optionValue);
      setSelectedValue(optionValue);
      onValueChange(optionValue);
      setIsOpen(false);
    };

    const selectedOption = options.find(option => option.value === selectedValue);

    return (
      <div className={cn("relative", className)} ref={ref}>
        <button
          type="button"
          id={id}
          className={cn(
            "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background",
            "placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
            "disabled:cursor-not-allowed disabled:opacity-50"
          )}
          onClick={() => setIsOpen(!isOpen)}
          aria-expanded={isOpen}
          aria-haspopup="listbox"
        >
          <span className={cn(selectedValue ? "text-foreground" : "text-muted-foreground")}>
            {selectedOption ? selectedOption.label : placeholder}
          </span>
          <ChevronDown className={cn("h-4 w-4 opacity-50 transition-transform", isOpen && "rotate-180")} />
        </button>

        {isOpen && (
          <>
            {/* Mobile overlay */}
            {(isMobile || isTouchDevice) && (
              <div 
                className="fixed inset-0 z-40 bg-black/20 backdrop-blur-sm"
                onClick={() => setIsOpen(false)}
              />
            )}
            
            <div 
              ref={dropdownRef}
              className={cn(
                "z-50 rounded-md border bg-popover text-popover-foreground shadow-md mobile-scroll",
                (isMobile || isTouchDevice)
                  ? "fixed left-4 right-4 bottom-4 max-h-[50vh] overflow-y-auto" 
                  : "absolute top-full left-0 right-0 mt-1 max-h-60 overflow-auto"
              )}
            >
              <div className="p-1">
                {/* Mobile header */}
                {(isMobile || isTouchDevice) && (
                  <div className="sticky top-0 bg-popover border-b border-border p-3 mb-1">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sm">{placeholder}</span>
                      <button
                        onClick={() => setIsOpen(false)}
                        className="text-muted-foreground hover:text-foreground mobile-touch-target"
                      >
                        <ChevronDown className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                )}
                
                {options.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    className={cn(
                      "relative flex w-full cursor-pointer select-none items-center rounded-sm outline-none",
                      "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                      selectedValue === option.value && "bg-accent text-accent-foreground",
                      (isMobile || isTouchDevice) ? "py-3 pl-8 pr-4 text-base mobile-touch-target" : "py-1.5 pl-8 pr-2 text-sm"
                    )}
                    onClick={() => handleSelect(option.value)}
                  >
                    <span className={cn(
                      "absolute flex items-center justify-center",
                      (isMobile || isTouchDevice) ? "left-3 h-4 w-4" : "left-2 h-3.5 w-3.5"
                    )}>
                      {selectedValue === option.value && <Check className="h-4 w-4" />}
                    </span>
                    {option.label}
                  </button>
                ))}
                
                {/* Mobile footer with reset option */}
                {(isMobile || isTouchDevice) && (
                  <div className="sticky bottom-0 bg-popover border-t border-border p-2 mt-1">
                    <button
                      onClick={() => handleSelect('')}
                      className="w-full py-2 px-3 text-sm text-muted-foreground hover:text-foreground hover:bg-accent rounded-sm mobile-touch-target"
                    >
                      Limpar seleção
                    </button>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    );
  }
);

CustomSelect.displayName = "CustomSelect";