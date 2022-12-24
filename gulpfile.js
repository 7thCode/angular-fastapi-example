const gulp = require('gulp');

gulp.task('build', () => {

    return gulp.src([
        'logs/*',
        'public/**/*',
        'server/**/*.py',
        'main.py',
        'package.json',
        'package-lock.json',
        'Pipfile',
        'Pipfile.lock',

    ], {base: './', allowEmpty: true})
        .pipe(gulp.dest('product'));

});




gulp.task('default', gulp.series('build'), () => {

});
