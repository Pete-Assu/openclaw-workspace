import('./libs/skill-scanner.js').then(async ({ scanMoltbook, scanGitHub, scanClawHub, scanAllPlatforms }) => {
  console.log('Test 1: Moltbook');
  const m = await scanMoltbook(5);
  console.log(`   Found ${m.length} posts\n`);

  console.log('Test 2: GitHub');
  const g = await scanGitHub();
  console.log(`   Found ${g.length} repos\n`);

  console.log('Test 3: All Platforms');
  const all = await scanAllPlatforms();
  console.log(`   Found ${all.length} total\n`);

  console.log('Done');
});
