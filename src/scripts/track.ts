// Umami custom events, for clicks the page handles itself (the drawer, the hero stack). Links
// that leave the page carry data-umami-event attributes instead. Not those that open the drawer:
// Umami cancels a tagged same-tab link's click and follows the link itself, so the page would
// load /work/<name> instead of opening the drawer. Does nothing while the script is blocked or
// still loading.
type Umami = { track: (name: string, data?: Record<string, string>) => void };

export const track = (name: string, data?: Record<string, string>) => {
  try {
    (window as Window & { umami?: Umami }).umami?.track(name, data);
  } catch {
    // Analytics never gets in the way of the page.
  }
};
