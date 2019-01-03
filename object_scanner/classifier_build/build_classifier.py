from rubik.train_server import TrainServer
from rubik.external_storage import ExternalStorage
from rubik.project_configurator import ProjectConfigurator
from rubik.train_decorator import build_phase, schedule_phase, get_results_phase
from shutil import copyfile
from subprocess import STDOUT, check_output
import time
import logging
import os
import glob

working_dir = 'temp'
task_name = 'task_build_classifier'


def build():
    """
        Run this method on AI server only, after this ends you could find the results using get_results
        method
    """
    nas2 = ExternalStorage('nas2')

    res = check_output(["git", "clone", "https://github.com/mrnugget/opencv-haar-classifier-training"])
    print(res)

    # download negative images
    if not nas2.download('build_classifier/door/sample_negative_images', 'opencv-haar-classifier-training/'):
        print('Cannot download negative images from nas2')
        return

    # download sample images
    if not nas2.download('build_classifier/door/samples', 'opencv-haar-classifier-training/'):
        print('Cannot download samples from nas')
        return

    # create negatives.txt file
    os.system('cd opencv-haar-classifier-training && find ./sample_negative_images -iname \"*.png\" > ./negatives.txt')

    negative_files_count = len(glob.glob('opencv-haar-classifier-training/sample_negative_images/*.png'))
    sample_files_count = len(glob.glob('opencv-haar-classifier-training/samples/*.png'))

    print('There are', negative_files_count, 'negative images')
    print('There are', sample_files_count, 'sample images')

    # create cropped.vec file
    print('Proceed to create .vec file')

    start_time = time.time()
    cmd = 'cd opencv-haar-classifier-training/samples && ' + \
          'opencv_createsamples ' + \
          '-info cropped.txt ' + \
          '-bg ../negatives.txt ' + \
          '-vec cropped.vec ' + \
          '-num ' + str(sample_files_count) + ' -w 70 -h 70'

    prog = check_output(str(cmd), shell=True, stderr=STDOUT, timeout=100)

    print('Out', prog.decode())
    print('The process took', int(time.time() - start_time) % 60, 'seconds')

    # copy cropped vector in order to be able to debug - view images from vec file
    cropped_vec_path = 'opencv-haar-classifier-training/samples/cropped.vec'

    cropped_vec_path = ProjectConfigurator.get_path_from_storage(cropped_vec_path)
    copyfile(cropped_vec_path, ProjectConfigurator.get_path_from_storage('/') + '/cropped.vec')

    negative_files_count = int(0.9 * negative_files_count)
    sample_files_count = int(0.9 * sample_files_count)

    # start build classifier
    print('Start build classifier')

    start_time = time.time()
    cmd = 'cd opencv-haar-classifier-training && ' + \
          'opencv_traincascade -data classifier ' + \
          '-vec samples/cropped.vec ' + \
          '-bg negatives.txt ' + \
          '-numPos ' + str(sample_files_count) + ' -numNeg ' + str(negative_files_count) + ' -numStages 10 ' + \
          '-precalcValBufSize 1024 -precalcIdxBufSize 1024 ' + \
          '-featureType HAAR ' + \
          '-minHitRate 0.995 -maxFalseAlarmRate 0.5 ' + \
          '-w 70 -h 70'

    prog = check_output(str(cmd), shell=True, stderr=STDOUT, timeout=72000)

    print('Out', prog.decode())
    print('The process took', int(time.time() - start_time) % 60, 'seconds')

    # Copy the classifier into storage
    classifier_file_path =\
        ProjectConfigurator.get_path_from_storage('opencv-haar-classifier-training/classifier/cascade.xml')
    copyfile(classifier_file_path, 'cascade.xml')

    # remove working data from storage
    # ProjectConfigurator.remove_path_from_storage('opencv-haar-classifier-training')


def schedule():
    """
        Schedule task to remote AI server
    """
    print('Schedule build classifier task')
    # schedule task before execute
    ai_server = TrainServer()

    # schedule a task
    ret, _, _ = ai_server.schedule_task(
        task_name=task_name,
        async=True)

    if not ret:
        print('Cannot schedule task')
        return

    print('Task successfully scheduled')


def results():
    """
        Get task results from AI server
    """
    build_path = working_dir + '/classifier_builds'
    print('Get build classifier task status')
    ai_server = TrainServer()

    ret, statuses = ai_server.task_status(task_name)

    if not ret:
        print('Cannot get task statuses')
        return

    for task_build, task_status in statuses.items():
        print('task_name:', task_name, 'task_build:', task_build, 'status:', task_status)
        if task_status in ['ok', 'failed']:
            # proceed to download task results
            ret, output_path = ai_server.get_unpacked_task_output(task_build, build_path + '/' + task_build)
            if ret:
                print('Task [', task_build, '] successfully downloaded into [', output_path, ']')
                
                # Copy cropped.vec file into workarea
                cropped_vec_from_path =\
                    ProjectConfigurator.get_path_from_storage(build_path + '/' + task_build + '/cropped.vec')
                cropped_vec_to_path = ProjectConfigurator.get_path_from_storage('temp') + '/cropped.vec' 
                copyfile(cropped_vec_from_path, cropped_vec_to_path)

                # copy cascade.xml file into classifier
                cascade_xml_from_path =\
                    ProjectConfigurator.get_path_from_storage(build_path + '/' + task_build + '/cascade.xml')
                cascade_xml_to_path = ProjectConfigurator.get_path_from_storage('classifier') + '/cascade.xml'
                copyfile(cascade_xml_from_path, cascade_xml_to_path)

    if len(statuses) == 0:
        print('There are no builds in progress')


@get_results_phase
def get_results_phase():
    # set logging
    logging.basicConfig(level=logging.WARNING)

    # get results
    results()


@schedule_phase
def schedule_phase():
    # set logging
    logging.basicConfig(level=logging.WARNING)

    # schedule task
    schedule()


@build_phase
def build_phase():
    # set logging
    logging.basicConfig(level=logging.DEBUG)

    # build task
    build()


def main():
    """
        The following argv could be used:
            -p get_results (in order to get results about the task from remote)
            -p schedule (in order to schedule task on remote AI server)
            -p build (in order to start building the task - not recommended on local)
    """

    # Only one should be run
    schedule_phase()

    # Get last executed task results
    get_results_phase()

    try:
        build_phase()
    except Exception as err:
        print('Error: [' + str(err) + ']')
        # ProjectConfigurator.remove_path_from_storage('opencv-haar-classifier-training')


if __name__ == '__main__':
    main()
