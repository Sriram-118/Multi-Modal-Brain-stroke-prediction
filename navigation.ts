/**
 * Navigation Component
 * Handles active page indication and navigation state management
 */

import { NavigationItem } from '../types';

export class NavigationManager {
  private navContainer: HTMLElement;
  private currentPath: string;
  private navItems: Map<string, HTMLElement>;

  constructor(navContainerSelector: string = '.navbar-nav') {
    const container = document.querySelector(navContainerSelector);
    if (!container) {
      throw new Error(`Navigation container not found: ${navContainerSelector}`);
    }
    
    this.navContainer = container as HTMLElement;
    this.currentPath = window.location.pathname;
    this.navItems = new Map();
    
    this.init();
  }

  private init(): void {
    this.collectNavItems();
    this.setActiveState();
    this.setupEventListeners();
  }

  private collectNavItems(): void {
    const links = this.navContainer.querySelectorAll('.nav-link:not(.dropdown-toggle)');
    
    links.forEach((link) => {
      const htmlLink = link as HTMLAnchorElement;
      const href = htmlLink.getAttribute('href');
      
      if (href) {
        this.navItems.set(href, htmlLink);
      }
    });
  }

  private setActiveState(): void {
    // Clear all active states first
    this.clearAllActiveStates();
    
    // Set active state for current page
    this.navItems.forEach((link, href) => {
      if (this.isCurrentPage(href)) {
        this.setActive(link);
      }
    });
  }

  private clearAllActiveStates(): void {
    this.navItems.forEach((link) => {
      this.setInactive(link);
    });
  }

  private isCurrentPage(href: string): boolean {
    try {
      const linkUrl = new URL(href, window.location.origin);
      const currentUrl = new URL(window.location.href);
      
      // Exact match for most pages
      if (linkUrl.pathname === currentUrl.pathname) {
        return true;
      }
      
      // Special handling for Django URL patterns
      const specialMatches = [
        // Handle .html extensions
        { pattern: /\.html$/, match: (link: string, current: string) => 
          link.replace('.html', '') === current || link === current + '.html' },
        
        // Handle action URLs (like PredictAction -> Predict.html)
        { pattern: /Action$/, match: (link: string, current: string) => 
          current.includes(link.replace('Action', '')) },
        
        // Handle base URLs
        { pattern: /\/$/, match: (link: string, current: string) => 
          link.slice(0, -1) === current || link === current + '/' }
      ];
      
      for (const { pattern, match } of specialMatches) {
        if (pattern.test(linkUrl.pathname) || pattern.test(currentUrl.pathname)) {
          if (match(linkUrl.pathname, currentUrl.pathname)) {
            return true;
          }
        }
      }
      
      return false;
    } catch (error) {
      console.warn('Error comparing URLs:', error);
      return href === this.currentPath;
    }
  }

  private setActive(link: HTMLElement): void {
    link.classList.add('active');
    link.setAttribute('aria-current', 'page');
    
    const navItem = link.closest('.nav-item');
    if (navItem) {
      navItem.classList.add('active');
    }
    
    // Add visual indicator
    this.addActiveIndicator(link);
  }

  private setInactive(link: HTMLElement): void {
    link.classList.remove('active');
    link.removeAttribute('aria-current');
    
    const navItem = link.closest('.nav-item');
    if (navItem) {
      navItem.classList.remove('active');
    }
    
    // Remove visual indicator
    this.removeActiveIndicator(link);
  }

  private addActiveIndicator(link: HTMLElement): void {
    // Add a subtle visual indicator for the active page
    const indicator = document.createElement('span');
    indicator.className = 'active-indicator';
    indicator.setAttribute('aria-hidden', 'true');
    indicator.innerHTML = '<i class="fas fa-circle" style="font-size: 0.5rem; margin-left: 0.5rem; opacity: 0.7;"></i>';
    
    // Remove existing indicator first
    this.removeActiveIndicator(link);
    
    // Add new indicator
    link.appendChild(indicator);
  }

  private removeActiveIndicator(link: HTMLElement): void {
    const existingIndicator = link.querySelector('.active-indicator');
    if (existingIndicator) {
      existingIndicator.remove();
    }
  }

  private setupEventListeners(): void {
    // Listen for navigation clicks
    this.navItems.forEach((link) => {
      link.addEventListener('click', (event) => {
        this.handleNavClick(event, link);
      });
    });

    // Listen for popstate events (browser back/forward)
    window.addEventListener('popstate', () => {
      this.currentPath = window.location.pathname;
      this.setActiveState();
    });

    // Listen for hash changes
    window.addEventListener('hashchange', () => {
      this.setActiveState();
    });
  }

  private handleNavClick(event: Event, link: HTMLElement): void {
    const href = (link as HTMLAnchorElement).href;
    
    // Don't interfere with external links or special links
    if (href.startsWith('javascript:') || href.includes('#') || 
        (link as HTMLAnchorElement).target === '_blank') {
      return;
    }
    
    // Update active state immediately for better UX
    this.clearAllActiveStates();
    this.setActive(link);
    
    // Close mobile menu if open
    this.closeMobileMenu();
  }

  private closeMobileMenu(): void {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
      const bsCollapse = (window as any).bootstrap?.Collapse;
      if (bsCollapse) {
        const collapse = new bsCollapse(navbarCollapse, { toggle: false });
        collapse.hide();
      }
    }
  }

  // Public methods for external control
  public updateActiveState(): void {
    this.currentPath = window.location.pathname;
    this.setActiveState();
  }

  public setActiveByHref(href: string): void {
    const link = this.navItems.get(href);
    if (link) {
      this.clearAllActiveStates();
      this.setActive(link);
    }
  }

  public getActiveLink(): HTMLElement | null {
    for (const [, link] of this.navItems) {
      if (link.classList.contains('active')) {
        return link;
      }
    }
    return null;
  }

  public getNavigationItems(): NavigationItem[] {
    const items: NavigationItem[] = [];
    
    this.navItems.forEach((link, href) => {
      const icon = link.querySelector('i');
      const text = link.textContent?.trim() || '';
      
      items.push({
        label: text,
        url: href,
        icon: icon?.className,
        active: link.classList.contains('active'),
        requiresAuth: this.isAuthRequiredLink(link)
      });
    });
    
    return items;
  }

  private isAuthRequiredLink(link: HTMLElement): boolean {
    const href = (link as HTMLAnchorElement).href;
    const authRequiredPaths = ['/LoadDataset', '/TrainModels', '/Predict'];
    
    return authRequiredPaths.some(path => href.includes(path));
  }
}

/**
 * Breadcrumb Manager
 * Handles breadcrumb navigation generation and updates
 */
export class BreadcrumbManager {
  private breadcrumbContainer: HTMLElement | null;
  private pathMappings: Map<string, string>;

  constructor() {
    this.breadcrumbContainer = document.querySelector('.breadcrumb');
    this.pathMappings = new Map([
      ['/', 'Home'],
      ['/UserLogin.html', 'Login'],
      ['/Register.html', 'Register'],
      ['/Predict.html', 'Predict Disease'],
      ['/LoadDataset', 'Dataset'],
      ['/TrainModels', 'Train Models']
    ]);
  }

  public generateBreadcrumbs(): void {
    if (!this.breadcrumbContainer) return;

    const currentPath = window.location.pathname;
    const breadcrumbs = this.buildBreadcrumbPath(currentPath);
    
    this.renderBreadcrumbs(breadcrumbs);
  }

  private buildBreadcrumbPath(path: string): Array<{title: string, url?: string}> {
    const breadcrumbs = [{ title: 'Home', url: '/' }];
    
    if (path !== '/' && path !== '') {
      const title = this.pathMappings.get(path) || this.generateTitleFromPath(path);
      breadcrumbs.push({ title });
    }
    
    return breadcrumbs;
  }

  private generateTitleFromPath(path: string): string {
    // Remove leading slash and file extensions
    let title = path.replace(/^\//, '').replace(/\.(html|php)$/, '');
    
    // Convert camelCase or snake_case to Title Case
    title = title.replace(/([A-Z])/g, ' $1')
                 .replace(/_/g, ' ')
                 .replace(/\b\w/g, l => l.toUpperCase())
                 .trim();
    
    return title || 'Page';
  }

  private renderBreadcrumbs(breadcrumbs: Array<{title: string, url?: string}>): void {
    if (!this.breadcrumbContainer) return;

    this.breadcrumbContainer.innerHTML = '';
    
    breadcrumbs.forEach((crumb, index) => {
      const li = document.createElement('li');
      li.className = 'breadcrumb-item';
      
      if (index === breadcrumbs.length - 1) {
        // Last item (current page)
        li.className += ' active';
        li.setAttribute('aria-current', 'page');
        li.textContent = crumb.title;
      } else {
        // Linked items
        const link = document.createElement('a');
        link.href = crumb.url || '#';
        link.className = 'text-decoration-none';
        link.textContent = crumb.title;
        
        if (crumb.title === 'Home') {
          link.innerHTML = '<i class="fas fa-home me-1" aria-hidden="true"></i>' + crumb.title;
        }
        
        li.appendChild(link);
      }
      
      this.breadcrumbContainer.appendChild(li);
    });
  }

  public addPathMapping(path: string, title: string): void {
    this.pathMappings.set(path, title);
  }

  public updateBreadcrumbs(): void {
    this.generateBreadcrumbs();
  }
}

// Export for global access
declare global {
  interface Window {
    StrokeApp: {
      NavigationManager: typeof NavigationManager;
      BreadcrumbManager: typeof BreadcrumbManager;
      [key: string]: any;
    };
  }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  try {
    const navManager = new NavigationManager();
    const breadcrumbManager = new BreadcrumbManager();
    
    // Make available globally
    window.StrokeApp = window.StrokeApp || {};
    window.StrokeApp.NavigationManager = NavigationManager;
    window.StrokeApp.BreadcrumbManager = BreadcrumbManager;
    window.StrokeApp.navManager = navManager;
    window.StrokeApp.breadcrumbManager = breadcrumbManager;
    
    // Generate breadcrumbs if container exists
    breadcrumbManager.generateBreadcrumbs();
    
  } catch (error) {
    console.warn('Navigation initialization failed:', error);
  }
});