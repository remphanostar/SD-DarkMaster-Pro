console.log('Popup script starting...');

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM Content Loaded - Test Version');
  
  // Test basic button functionality
  const testBtn = document.createElement('button');
  testBtn.textContent = 'Test Button';
  testBtn.style.cssText = 'padding: 10px; margin: 10px; background: red; color: white;';
  testBtn.addEventListener('click', () => {
    console.log('Test button clicked!');
    alert('Test button works!');
  });
  
  // Add test button to body
  document.body.appendChild(testBtn);
  
  // Try to get existing buttons
  const addFolderBtn = document.getElementById('addFolderBtn');
  const importFileBtn = document.getElementById('importFileBtn');
  
  console.log('Existing buttons found:', { addFolderBtn, importFileBtn });
  
  if (addFolderBtn) {
    console.log('Adding event listener to addFolderBtn');
    addFolderBtn.addEventListener('click', () => {
      console.log('Add Folder button clicked!');
      alert('Add Folder button works!');
    });
  }
  
  if (importFileBtn) {
    console.log('Adding event listener to importFileBtn');
    importFileBtn.addEventListener('click', () => {
      console.log('Import File button clicked!');
      alert('Import File button works!');
    });
  }
  
  console.log('Test script initialization complete');
});