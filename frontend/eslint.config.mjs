import pluginJs from '@eslint/js'
import pluginNext from '@next/eslint-plugin-next'
import stylistic from '@stylistic/eslint-plugin'
import stylisticTs from '@stylistic/eslint-plugin-ts'
import tsParser from '@typescript-eslint/parser'
import eslintConfigPrettier from 'eslint-config-prettier'
import importPlugin from 'eslint-plugin-import'
import react from 'eslint-plugin-react'
import pluginReactHooks from 'eslint-plugin-react-hooks'
import unusedPlugin from 'eslint-plugin-unused-imports'
import globals from 'globals'
import tseslint from 'typescript-eslint'

/** @type {import('eslint').Linter.Config[]} */
export default [
  { files: ['**/*.{js,mjs,cjs,ts,jsx,tsx}'] },
  { languageOptions: { globals: globals.browser, parser: tsParser } },
  { linterOptions: { reportUnusedDisableDirectives: 'error' } },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  react.configs.flat.recommended,
  react.configs.flat['jsx-runtime'],
  eslintConfigPrettier,
  {
    plugins: {
      react,
      'react-hooks': pluginReactHooks,
      'import': importPlugin,
      'unused-imports': unusedPlugin,
      '@next/next': pluginNext,
      '@stylistic': stylistic,
      '@stylistic/ts': stylisticTs,
    }
  },
  {
    ignores: ['.storybook/*', 'src/stories/*', 'src/**/*.stories.tsx', 'dist'],
    settings: { react: { pragma: 'React', fragment: 'Fragment', version: '18.3' } },
    rules: {
      ...pluginNext.configs.recommended.rules,
      indent: ['error', 2], // インデントを2スペースで強制
      semi: ['error', 'never'], // セミコロンを不要に
      quotes: ['error', 'single'], // シングルクォートを強制
      eqeqeq: ['error', 'always'], // 厳密な等価演算子を強制
      complexity: ['warn', { max: 15 }], // 関数の複雑さを制限
      camelcase: ['error', { properties: 'always' }], // キャメルケースを強制
      'no-var': ['error'], // var の使用を禁止
      'no-undef': ['off'],
      'no-console': ['warn'], // console.log の使用を警告
      'no-unused-vars': ['off'], // 未使用の変数をエラーとして検出
      'no-magic-numbers': ['warn', { ignore: [0, 1] }], // マジックナンバーの使用を警告
      'no-multiple-empty-lines': ['error', { max: 1, maxBOF: 0 }],
      'prefer-const': ['error'], // 再代入されない変数に const を推奨
      'consistent-return': ['error'], // 一貫した return を強制
      'brace-style': ['error', '1tbs'], // ブレースのスタイルを 1tbs に強制
      'comma-spacing': ['error', { before: false, after: true }], // カンマの後にスペースを強制
      'key-spacing': ['error', { beforeColon: false, afterColon: true }], // キーとコロンの間隔を設定
      'array-bracket-spacing': ['error', 'never'], // 配列の括弧内にスペースを禁止
      'object-curly-spacing': ['error', 'always'], // オブジェクトの中括弧内にスペースを強制
      'arrow-spacing': ['error', { before: true, after: true }], // アロー関数の矢印前後にスペースを強制
      'space-in-parens': ['error', 'never'], // 丸括弧内にスペースを禁止
      'func-call-spacing': ['error', 'never'], // 関数呼び出し時の関数名と括弧の間にスペースを禁止
      'eol-last': ['error', 'always'], // ファイル末尾に空行を強制
      'spaced-comment': ['error', 'always', { markers: ['/'] }], // コメントの開始にスペースを強制
      'linebreak-style': ['error', 'unix'], // 改行スタイルをLFに強制
      'react/jsx-uses-react': 'off',
      'react/react-in-jsx-scope': 'off',
      'react-hooks/exhaustive-deps': 'warn',
      '@stylistic/space-infix-ops': 'error', // 演算子の前後にスペースを強制
      '@stylistic/ts/space-infix-ops': 'error', // TypeScript特有のフォーマット設定も追加
      '@typescript-eslint/no-unused-expressions': 'off',
      '@typescript-eslint/no-require-imports': 'off',
      'unused-imports/no-unused-imports': 'error',
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
            { pattern: 'api/**', group: 'internal', position: 'before' },
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
    }
  }
]
