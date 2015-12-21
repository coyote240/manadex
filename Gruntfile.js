module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            development: {
                paths: ['assets/less'],
                compress: true,
                sourceMap: true,
                files: [{
                    src: 'assets/less/**/*.less', dest: 'assets/css/app.css'
                }]
            }
        },
        watch: {
            less: {
                files: 'assets/less/**/*.less',
                tasks: ['less']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default', ['less:development']);
};
