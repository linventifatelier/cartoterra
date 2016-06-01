module.exports = function(grunt){
    'use strict';

    require("matchdep").filterDev("grunt-*").forEach(grunt.loadNpmTasks);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        clean: {
            build: ['build'],
            release: ['release']
        },

        watch: {
            js: {
                files: ['assets/js/*.js'],
                tasks: ['concat:js_frontend','uglify']
            }
        },

        bower: {
            install: {
                options: {
                    copy: false
                }
            }
        },

        //concat: {
        //  options: {
        //    separator: ';',
        //  },
        //  js_frontend: {
        //    src: [
        //      //'./bower_components/jquery/jquery.js',
        //      //'./bower_components/bootstrap/dist/js/bootstrap.js',
        //      './assets/js/base.js',
        //      './assets/js/test.js'
        //    ],
        //    dest: './build/js/frontend.js',
        //  },
        //  //js_backend: {
        //  //  src: [
        //  //    './bower_components/jquery/jquery.js',
        //  //    './bower_components/bootstrap/dist/js/bootstrap.js',
        //  //    './app/assets/javascript/backend.js'
        //  //  ],
        //  //  dest: './public/assets/javascript/backend.js',
        //  //},
        //},

        csslint: {
            lax: {
                src: ['bower_components/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css']
            },
        },

        cssmin: {
            minify: {
                expand: true,
                flatten: true,
                src: ['bower_components/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
                      'bower_components/bootstrap/dist/css/bootstrap.css',
                      'bower_components/blueimp-gallery/css/blueimp-gallery.min.css',
                      'bower_components/leaflet/dist/leaflet.css',
                      'bower_components/leaflet.markercluster/dist/MarkerCluster.css',
                      'build/css/MarkerClusterDefault.css'
                      ],
                dest: 'build/css/',
                ext: '.min.css'

            }
        },

        uglify: {
            options: {
                preserveComments: 'some',
            },
            build: {
                files: {
                    // blueimp-gallery
                    'build/js/blueimp-gallery.min.js': ['bower_components/blueimp-gallery/js/blueimp-gallery.min.js'],
                    // bootstrap-datepicker
                    'build/js/bootstrap-datepicker.min.js': ['bower_components/bootstrap-datepicker/js/bootstrap-datepicker.js'],
                    // spin.js
                    'build/js/spin.min.js': ['bower_components/spin.js/spin.js'],
                    // openlayers
                    //'build/js/OpenLayers.min.js': ['bower_components/openlayers/build/OpenLayers.js'],
                    // leaflet
                    'build/js/leaflet.min.js': ['bower_components/leaflet/dist/leaflet.js'],
                    // leaflet.markercluster
                    'build/js/leaflet.markercluster.min.js': ['bower_components/leaflet.markercluster/dist/leaflet.markercluster.js'],
                    // bootstrap
                    'build/js/bootstrap.min.js': ['bower_components/bootstrap/dist/js/bootstrap.min.js'],
                    // html5shiv
                    'build/js/html5shiv.min.js': ['bower_components/html5shiv/dist/html5shiv.js'],
                    // jquery
                    // 'build/js/jquery.min.js': ['bower_components/jquery/dist/jquery.min.js'],
                    // exif-js
                    'build/js/exif.min.js': ['bower_components/exif-js/exif.js'],
                }
            }
        },

        copy: {
            main: {
                files: [
                    // blueimp-gallery
                    {expand: true, flatten: true, src: ['build/js/blueimp-gallery.min.js'], dest: 'release/geodata/js/'},
                    {expand: true, flatten: true, src: ['build/css/blueimp-gallery.min.css'], dest: 'release/geodata/css/'},
                    {expand: true, flatten: true, src: ['bower_components/blueimp-gallery/img/*'], dest: 'release/geodata/img/'},
                    // bootstrap-datepicker
                    {expand: true, flatten: true, src: ['build/js/bootstrap-datepicker.min.js'], dest: 'release/geodata/js/'},
                    {expand: true, flatten: true, src: ['build/css/bootstrap-datepicker3.min.css'], dest: 'release/geodata/css/'},
                    {expand: true, flatten: true, src: ['bower_components/bootstrap-datepicker/js/locales/*'], dest: 'release/geodata/js/locales/'},
                    // spin.js
                    {expand: true, flatten: true, src: ['build/js/spin.min.js'], dest: 'release/geodata/js/'},
                    // leaflet
                    {expand: true, flatten: true, src: ['build/js/leaflet.min.js'], dest: 'release/geodata/js/'},
                    {expand: true, flatten: true, src: ['build/css/leaflet.min.css'], dest: 'release/geodata/css/'},
                    {expand: true, flatten: true, src: ['bower_components/leaflet/dist/images/*'], dest: 'release/geodata/img/'},
                    // leaflet.markercluster
                    {expand: true, flatten: true, src: ['build/js/leaflet.markercluster.min.js'], dest: 'release/geodata/js/'},
                    {expand: true, flatten: true, src: ['build/css/MarkerCluster.min.css'], dest: 'release/geodata/css/'},
                    {expand: true, flatten: true, src: ['build/css/MarkerClusterDefault.min.css'], dest: 'release/geodata/css/'},
                    // bootstrap
                    {expand: true, flatten: true, src: ['build/js/bootstrap.min.js'], dest: 'release/cartoterra/js/'},
                    {expand: true, flatten: true, src: ['build/css/bootstrap.min.css'], dest: 'release/cartoterra/css/'},
                    {expand: true, flatten: true, src: ['bower_components/bootstrap/dist/fonts/*'], dest: 'release/cartoterra/fonts/'},
                    // html5shiv
                    {expand: true, flatten: true, src: ['build/js/html5shiv.min.js'], dest: 'release/cartoterra/js/'},
                    // jquery
                    // {expand: true, flatten: true, src: ['build/js/jquery.min.js'], dest: 'release/js/'},
                    {expand: true, flatten: true, src: ['bower_components/jquery/dist/jquery.min.js'], dest: 'release/cartoterra/js/'},
                    // exif-js
                    {expand: true, flatten: true, src: ['build/js/exif.min.js'], dest: 'release/cartoterra/js/'},
                ]
            },
            markercluster: {
                src: 'bower_components/leaflet.markercluster/dist/MarkerCluster.Default.css',
                dest: 'build/css/MarkerClusterDefault.css'
            },
            deploy: {
                files: [
                    {expand: true, cwd: 'release/cartoterra/', src: ['**'], dest: '../cartoterra/static/'},
                    {expand: true, cwd: 'release/geodata/', src: ['**'], dest: '../geodata/static/'},
                ]
            }
        },
    });

    grunt.registerTask('build', ['clean', 'bower:install', 'copy:markercluster', 'cssmin', 'uglify', 'copy:main']);
    grunt.registerTask('deploy', ['copy:deploy']);
    grunt.registerTask('default', ['build', 'deploy']);

};
