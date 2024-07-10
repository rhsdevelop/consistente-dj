const gulp = require('gulp');
const { simpleGit } = require('simple-git');
const { execSync } = require('child_process');
const { version } = require('./utils');

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
|   Make Product
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
const git = simpleGit();

gulp.task('pre:live', async () => {
  const branch = await git.branch();
  const currentBranch = branch.current;

  const status = await git.status();
  const isClean = await status.isClean();

  if (isClean) {
    await git.checkout('live');
    await git.pull();
    await git.merge([currentBranch]);
  } else {
    throw new Error('error');
  }
});

gulp.task('post:live', async () => {
  execSync('npm run live');
  await git.add('./*').commit(`live-${version}`);
  execSync('npm run publish');
  await git.checkout('develop');
});
