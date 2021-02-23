const path = require('../../package.json')

module.exports = {
    title: 'Dungeons Dragons Online',

    base: '/',

    head: [
        ['meta', { name: 'theme-color', content: '#b33939' }],
        ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
        ['meta',{ name: 'apple-mobile-web-app-status-bar-style', content: 'black' },],
    ],


    markdown: {
        lineNumbers: true
    },


    themeConfig: {
        repo: 'https://github.com/Sosso8305/dungeons-dragons-online',
        editLinks: true,
        docsDir: 'docs',
        docsBranch: 'master',
        lastUpdated: true,
        nav: [
            {
            text: 'Guides',
            link: '/guides/',
            },
        ],
        sidebar: {
            '/guides/': [
                {
                    title: 'online',
                    collapsable: false,
                    children: [
                    'online/',
                    'online/RESEAUX',
                    'online/InterfacePython',
                    'online/Peer2Peer',
                    'online/Connection_with_other',
                    ],
                },
            ],
        },
    },
    
}