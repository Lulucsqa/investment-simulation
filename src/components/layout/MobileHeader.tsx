import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Menu, Settings, HelpCircle } from 'lucide-react';
import { HelpCenter } from '../HelpCenter';

interface MobileHeaderProps {
  title: string;
  subtitle?: string;
  onShowOnboarding?: () => void;
}

export const MobileHeader: React.FC<MobileHeaderProps> = ({
  title,
  subtitle,
  onShowOnboarding,
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="md:hidden border-b bg-card/50 backdrop-blur-xl">
      <div className="flex items-center justify-between p-4">
        <div className="flex-1 min-w-0">
          <h1 className="text-lg font-bold text-rainbow truncate">
            {title}
          </h1>
          {subtitle && (
            <p className="text-sm text-muted-foreground truncate">
              {subtitle}
            </p>
          )}
        </div>

        <Sheet open={isMenuOpen} onOpenChange={setIsMenuOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="sm" className="p-2">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-80">
            <SheetHeader>
              <SheetTitle>Menu</SheetTitle>
            </SheetHeader>
            
            <div className="mt-6 space-y-4">
              {onShowOnboarding && (
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => {
                    onShowOnboarding();
                    setIsMenuOpen(false);
                  }}
                >
                  <Settings className="h-4 w-4 mr-2" />
                  Tour Guiado
                </Button>
              )}
              
              <div className="border-t pt-4">
                <div className="flex items-center gap-2 mb-3">
                  <HelpCircle className="h-4 w-4" />
                  <span className="font-medium">Central de Ajuda</span>
                </div>
                <HelpCenter />
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </div>
  );
};

export default MobileHeader;