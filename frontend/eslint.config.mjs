import pluginJs from '@eslint/js'
import stylisticTs from '@stylistic/eslint-plugin-ts'
import tsEsLintPlugin from '@typescript-eslint/eslint-plugin'
import importPlugin from 'eslint-plugin-import'
import pluginReact from 'eslint-plugin-react'
import pluginReactHooks from 'eslint-plugin-react-hooks'
import unusedPlugin from 'eslint-plugin-unused-imports'
import globals from 'globals'
import tseslint from 'typescript-eslint'

/** @type {import('eslint').Linter.Config[]} */
export default [
  { files: ['**/*.{js,mjs,cjs,ts,d.ts,jsx,tsx}'] },
  { languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,
  {
    plugins: {
      react: pluginReact,
      'react-hooks': pluginReactHooks,
      'import': importPlugin,
      'unused-imports': unusedPlugin,
      '@typescript-eslint': tsEsLintPlugin,
      '@stylistic/ts': stylisticTs,
    },
  },
  {
    rules: {
      semi: ['error', 'never'], // セミコロンを不要に
      indent: ['error', 2], // インデントを2スペースで強制
      quotes: ['error', 'single'], // シングルクォートを強制
      eqeqeq: ['error', 'always'], // 厳密な等価演算子を強制
      complexity: ['warn', { max: 20 }], // 関数の複雑さを制限
      camelcase: ['error', { properties: 'always' }], // キャメルケースを強制
      'no-console': ['warn'], // console.log の使用を警告
      'no-multi-spaces': ['error'], // 複数スペースを禁止
      'no-multiple-empty-lines': ['error', { max: 1, maxBOF: 0, maxEOF: 0 }], // 連続する空行を禁止
      'no-magic-numbers': ['off', { ignore: [0, 1, 2] }], // マジックナンバーの使用を警告
      'prefer-const': ['error'], // 再代入されない変数に const を強制
      'comma-dangle': ['error', 'always-multiline'], // 配列やオブジェクトの最後にカンマを強制
      'comma-spacing': ['error', { before: false, after: true }], // カンマの後にスペースを強制
      'space-infix-ops': ['error', { 'int32Hint': false }], // 演算子の前後にスペースを強制
      'space-in-parens': ['error', 'never'], // 丸括弧内にスペースを禁止
      'space-before-blocks': 'error', // ブロック開始の前にスペースを強制
      'space-before-function-paren': ['error', { 'anonymous': 'never', 'named': 'never', 'asyncArrow': 'always' }], // スペースの設定
      'spaced-comment': ['error', 'always', { markers: ['/'] }], // コメントの開始にスペースを強制
      'array-bracket-spacing': ['error', 'never'], // 配列の括弧内にスペースを禁止
      'key-spacing': ['error', { beforeColon: false, afterColon: true }], // キーとコロンの間隔を設定
      'keyword-spacing': 'error', // if文の括弧前にスペースを強制
      'arrow-spacing': ['error', { before: true, after: true }], // アロー関数の矢印前後にスペースを強制
      'func-call-spacing': ['error', 'never'], // 関数呼び出し時の関数名と括弧の間にスペースを禁止
      'object-curly-spacing': ['error', 'always'], // オブジェクトの中括弧内にスペースを強制
      'object-curly-newline': ['error', { 'consistent': true }], // オブジェクトの括弧内での改行を一貫性を持たせる
      'eol-last': ['error', 'always'], // ファイル末尾に空行を強制
      'react/jsx-uses-react': 'off', // Reactのimportが不要
      'react/react-in-jsx-scope': 'off', // Reactのimportが不要
      'react-hooks/exhaustive-deps': 'warn', // Hooksの依存配列で警告
      '@typescript-eslint/no-explicit-any': 'warn', // anyの使用を警告
      'unused-imports/no-unused-imports': 'error', // 未使用のimportを禁止
      'import/order': ['error',
        {
          groups: ['builtin', 'external', 'internal', ['parent', 'sibling', 'index']],
          alphabetize: { order: 'asc', caseInsensitive: false },
          'newlines-between': 'never',
          pathGroupsExcludedImportTypes: ['builtin'],
          pathGroups: [
            { pattern: '{react,react/**,react-dom/**,react-**}', group: 'builtin', position: 'before' },
            { pattern: '{next,next/**,next-i18next,next-i18next/**,next-**}', group: 'builtin', position: 'before' },
            { pattern: 'lib/**', group: 'internal', position: 'before' },
            { pattern: 'types/**', group: 'internal', position: 'before' },
            { pattern: '{api/**,api/external/**,api/internal/**}', group: 'internal', position: 'before' },
            { pattern: 'utils/**', group: 'internal', position: 'before' },
            { pattern: 'pages/**', group: 'internal', position: 'before' },
            { pattern: 'components/hooks/**', group: 'internal', position: 'before' },
            { pattern: 'components/provider/**', group: 'internal', position: 'before' },
            { pattern: '{components/layout,components/layout/**}', group: 'internal', position: 'before' },
            { pattern: 'components/parts/**', group: 'sibling', position: 'before' },
            { pattern: 'components/widgets/**', group: 'sibling', position: 'before' },
            { pattern: 'components/templates/**', group: 'sibling', position: 'before' },
          ],
        },
      ],
    },
  },
]
