// global.d.ts
interface Window {
  loadPyodide(config: any): Promise<any>;
}
