/* groovylint-disable CompileStatic, DuplicateStringLiteral*/

String blueOceanJobUrl() {
    return JOB_DISPLAY_URL
        .replaceFirst('job', 'blue/organizations/jenkins')
        .replace('job', 'detail')
        .replace('display/redirect', "${BUILD_NUMBER}/pipeline")
}

void setLastStage() {
    LAST_STAGE = STAGE_NAME
}

void discordNotify(Map params) {
    String webhookURL = params.webhookURL ?: DISCORD_WEBHOOK_URL
    String title = params.title ?: 'Build notification'
    String link = params.link ?: BLUE_OCEAN_JOB_URL
    String customUsername = params.customUsername ?: DISCORD_USERNAME
    String customAvatarUrl = params.customAvatarUrl ?: CHASERLAND_AVATAR_URL
    String description = params.description ?: 'No description'
    String footer = params.footer ?: BUILD_TITLE
    String result = params.result ?: 'SUCCESS'
    Boolean showChangeset = params.showChangeset ?: false

    discordSend(
        webhookURL: webhookURL,
        title: title,
        link: link,
        customUsername: customUsername,
        customAvatarUrl: customAvatarUrl,
        description: description,
        footer: footer,
        result: result,
        showChangeset: showChangeset
    )
}

pipeline {
    agent any
    options {
        buildDiscarder logRotator(
            artifactDaysToKeepStr: '15',
            artifactNumToKeepStr: '3',
            daysToKeepStr: '15',
            numToKeepStr: '30'
        )
        disableConcurrentBuilds()
        timeout(time: 10, unit: 'MINUTES')
        timestamps()
    }
    environment {
        BLUE_OCEAN_JOB_URL = ''
        COMMIT_SHA = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        VERSION = "${BRANCH_NAME}-${COMMIT_SHA}"
        DISCORD_WEBHOOK_URL = credentials('discord-webhook-url')
        CHASERLAND_AVATAR_URL = credentials('chaserland-avatar-url')
        LAST_STAGE = ''
        BUILD_TITLE = ''
        DURATION = ''
        DISCORD_USERNAME = 'ChaserLand CI'
    }
    stages {
        stage('pre-build') {
            steps {
                script {
                    setLastStage()
                    BLUE_OCEAN_JOB_URL = blueOceanJobUrl()
                    BUILD_TITLE = URLDecoder.decode(JOB_NAME, 'UTF-8')
                    echo "Branch: ${BRANCH_NAME}"
                }
                echo 'Sending build start message to Discord...'
                discordNotify(
                    title: "Build ${BUILD_TITLE} ${BUILD_DISPLAY_NAME} start!",
                    description: "Branch: <${BRANCH_NAME}>",
                    showChangeset: true
                )
            }
        }
        stage('Build prod') {
            when {
                branch 'main'
            }
            steps {
                script{
                    setLastStage()
                }
                echo 'Building main branch...'
            }
        }
        stage('Build dev') {
            when {
                branch 'dev'
            }
            steps {
                script{
                    setLastStage()
                }
                echo 'Building dev branch...'
            }
        }
        stage('Build feature/jenkins'){
            when {
                branch 'feature/jenkins'
            }
            steps {
                script{
                    setLastStage()
                }
                echo 'Building feature/jenkins branch...'
            }
        }
    }
    post {
        always {
            script {
                DURATION = currentBuild.durationString.replace('and counting', '')
            }
        }
        success {
            echo 'Sending build success message to Discord...'
            discordNotify(
                title: "Build ${BUILD_TITLE} ${BUILD_DISPLAY_NAME} success!",
                description: "Branch: <${BRANCH_NAME}>\nDuration: ${DURATION}",
                showChangeset: true
            )
        }
        failure {
            echo 'Build failed!'
            echo 'Sending build failed message to Discord...'
            discordNotify(
                title: "Build ${BUILD_TITLE} ${BUILD_DISPLAY_NAME} failed!",
                description: "Branch: <${BRANCH_NAME}>\nDuration: ${DURATION}",
                result: currentBuild.currentResult
            )
        }
        unstable {
            echo 'Build unstable!'
            echo 'Sending build unstable message to Discord...'
            discordNotify(
                title: "Build ${BUILD_TITLE} ${BUILD_DISPLAY_NAME} unstable!",
                description: "Branch: <${BRANCH_NAME}>\nDuration: ${DURATION}",
                result: currentBuild.currentResult
            )
        }
    }
}
